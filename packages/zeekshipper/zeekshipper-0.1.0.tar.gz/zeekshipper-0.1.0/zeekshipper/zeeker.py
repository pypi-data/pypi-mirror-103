import zat
import re
import s3fs
import click
import pandas as pd
import fastparquet
from zat.log_to_dataframe import LogToDataFrame
from pathlib import Path
from minio.error import S3Error
from minio import Minio

def create_bucket(buck_name,minio_ip,minio_port,access_key,secret_key):
    '''
    新建minio的桶
    '''
    client = Minio(
        "{}:{}".format(minio_ip,minio_port),
        secure=False,# 默认True[https]
        access_key=access_key,
        secret_key=secret_key,
    )

    found = client.bucket_exists(buck_name)
    if not found:
        client.make_bucket(buck_name)
        return '新建桶 {} 成功！'.format(buck_name)
    else:
        return "桶 '{}' 存在".format(buck_name)

def get_cmd(minio_dir_name,log_type,keys_str,schema_name,buck_name):
    '''
    格式化输出trino命令
    '''
    keys = re.findall("'(.*?)'",keys_str)
    keys.pop()
    kv=[]
    for ke in keys:
        if ke in ["object"]:
            continue
        if ke=='version':
            form = "BIGINT" if log_type in ['ntp'] else "VARCHAR"
        elif ke=='mail_from':
            form = "TIMESTAMP" if log_type in ['kerberos'] else "VARCHAR"
        elif ke in [
            'compile_ts',# 'ts_str','ts',
            'ref_time','org_time','rec_time','xmt_time', # ntp
            'till', # kerberos,
            'certificate_not_valid_before','certificate_not_valid_after', # x509
            'times_modified','times_accessed','times_created','times_changed', # smb_files
            ]:
            # time
            form = "TIMESTAMP"
        elif ke in [
            'year','month','day','id_orig_p','id_resp_p','file_size','reply_code','data_channel_resp_p', # ftp
            'dcc_file_size', # irc
            'mode','stratum','num_exts', # ntp
            'trans_id','qclass','qtype','rcode','Z', # dns
            'trans_depth', # smtp
            'depth','seen_bytes','total_bytes','missing_bytes','overflow_bytes','extracted_size', # files
            'orig_bytes','resp_bytes','missed_bytes','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes', # conn
            'certificate_version','certificate_key_length','basic_constraints_path_len', # x509
            'version','auth_attempts', # ssh
            'trans_depth','request_body_len','response_body_len','status_code','info_code', # http
            'p','n', # notice
            'size', # smb_files
        ]:
            # port,count
            form = "BIGINT"
        elif ke in [
            "data_channel_passive", # ftp 
            "success", # ntml、packet_filter、kerberos
            "is_exe","is_64bit","uses_aslr","uses_dep","uses_code_integrity","uses_seh",
            "has_import_table","has_export_table","has_cert_table","has_debug_data",# pe
            "rejected","AA","TC","RD","RA", # dns
            "init", # packet_filter
            "tls", # smtp
            "forwardable","renewable", # kerberos
            "local_orig","is_orig","timedout","extracted_cutoff", # files
            "local_orig","local_resp",# conn
            "notice", # weird
            "basic_constraints_ca", # x509
            "auth_success", # ssh
            "resumed","established", # ssl
        ]:
            # bool
            form = "BOOLEAN"
        elif ke in [
            'poll','precision','root_delay','root_disp', # ntp
            'rtt', # dns、sce_rpc
            'duration', # files、dhcp
            'lease_time', # dhcp
            'suppress_for','remote_location_latitude','remote_location_longitude', # notice
            ]:
            # INTERVAL(FLOAT)
            form = "DOUBLE"
        else:
            form = "VARCHAR"
        kv.append("""
        {} {}""".format(ke,form))
    out_cmd = """
    CREATE TABLE {}.{}.{} ({}
            ) 
            WITH (
            format='Parquet',
            partitioned_by = ARRAY['{}','{}','{}'],
            external_location = 's3://{}/{}/{}'
            );
    CALL system.sync_partition_metadata('{}','{}','FULL');
    SELECT * FROM {}.{}.{};
    """.format(buck_name,schema_name,log_type,",".join(kv),
                keys[-3],keys[-2],keys[-1],
                buck_name,minio_dir_name,log_type,
                schema_name,log_type,
                buck_name,schema_name,log_type)
    return out_cmd

def change_timedelta64_type(zeek_df):
    '''
    # 时间段数据 的类型转换为 float 
    '''
    for column in zeek_df.columns:
        if zeek_df[column].dtypes=='timedelta64[ns]':
            lie = []
            for onedel in zeek_df[column]:
                onedel_new = onedel.total_seconds()
                lie.append(onedel_new)
            zeek_df[column] = lie

def change_category_type(df):
    ''' 
    # category 类型转换为 bool
    '''
    for column in df.columns:
        pp = str(df[column].dtypes)
        if pp=='category':
            lie = []
            for onedel in df[column]:
                if onedel =="T":
                    onedel_new=True
                else:
                    onedel_new=False
                lie.append(onedel_new)
            df[column] = lie



@click.command()
@click.option('--buck_name', prompt='minio buck_name', help='minio中的桶名。')
@click.option('--local_path', prompt='local local_path', help='本地log文件所在文件夹路径。')
@click.option('--minio_dir_name', prompt='minio minio_dir_name', help='minio中用于存放parquet文件的文件夹路径。')
@click.option('--cmd_file', default='cmd.txt', help='输出trino命令的txt文件名（可加路径）。')
@click.option('--minio_ip', prompt='minio minio_ip', help='minio服务的ip。')
@click.option('--minio_port', prompt='minio minio_port', help='minio服务的port。')
@click.option('--schema_name', prompt='trino schema_name', help='trino中需要指定的schema名（数据库名）。')
@click.option('--access_key', prompt='minio access_key', help='用于minio登录的access_key。')
@click.option('--secret_key', prompt='minio secret_key', help='用于minio登录的secret_key。')
def log_minio_trino(buck_name,local_path,minio_dir_name,cmd_file,minio_ip,minio_port,schema_name,access_key,secret_key):
    '''
    buck_name   桶名
    local_path  本地log文件目录路径
    minio_dir_name  minio中用于放置数据的目录文件夹
    cmd_file    输出的trino命令.txt
    minio_ip    minio服务的ip
    minio_port  minio服务的port
    schema_name trino中指定的schema名
    access_key  用于minio登录的access_key
    secret_key  用于minio登录的secret_key
    '''
    create_mesage = create_bucket(buck_name=buck_name,minio_ip=minio_ip,minio_port=minio_port,
                                access_key=access_key,secret_key=secret_key)
    s3 = s3fs.S3FileSystem(
                      anon=False,
                      client_kwargs={'endpoint_url': 'http://{}:{}'.format(minio_ip,minio_port)},
                      key=access_key,
                      secret=secret_key
                     )
    log_to_df = LogToDataFrame()
    with open(cmd_file,'w') as f:
        f.write("+++++all cmd line+++++\n")

    for log in Path(local_path).glob('**/*.log'):
        log_type = log.parts[-1].split('.')[0]
        zeek_df = log_to_df.create_dataframe(log, ts_index=False, aggressive_category=False)

        # 列属性中的 . 转换为 _
        rename={}
        for it in zeek_df.keys():
            if it in ['date','from','to','path']:
                rename[it]="mail_"+it
                continue
            rename[it] = re.sub("\.","_",it,0,re.M|re.I)
        zeek_df = zeek_df.rename(columns=rename)
            
        # 时间段数据 的类型转换为 float 
        # category 类型转换为 bool
        change_timedelta64_type(zeek_df)
        change_category_type(zeek_df)
        
        # 把行属性（时间日期）中的日期单独建立列
        ts_lines = zeek_df['ts']
        # 转字符串
        zeek_df['ts'] = [da.isoformat() for da in ts_lines]
        # 避免 出现空数据变成浮点型 的处理
        zeek_df['year'] = pd.array(pd.DatetimeIndex(ts_lines).year, dtype="Int64")
        zeek_df['month'] = pd.array(pd.DatetimeIndex(ts_lines).month, dtype="Int64")
        zeek_df['day'] = pd.array(pd.DatetimeIndex(ts_lines).day, dtype="Int64")
                
        # 生成trino命令
        output_cmd = get_cmd(minio_dir_name=minio_dir_name,log_type=log_type,keys_str=str(zeek_df.keys()),schema_name=schema_name,buck_name=buck_name)
        if output_cmd:
            with open(cmd_file,'a') as f:
                f.write(output_cmd)

        # 写入minio
        try:
            fastparquet.write('{}/{}/{}'.format(buck_name,minio_dir_name,log_type),
                  zeek_df,
                  partition_on=['year', 'month', 'day'],
                  file_scheme='hive',
                  open_with=s3.open
                 )
            pass
        except:
            print(log, log_type)
            raise 

if __name__ == "__main__":
    lprint("hello!")