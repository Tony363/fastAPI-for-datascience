import boto3
import pandas as pd
from sagemaker import get_execution_role



def access_bucket(bucket,video_folder):
    data_location = 's3://{}/{}'.format(bucket,video_folder)
    tennis_bucket = s3_resource.Bucket(name=data_location)
    
    video_arr = list()
    for obj in tennis_bucket.objects.all():
        print(obj.Object())
        video_arr.append(obj.Object())
    return video_arr

def all_bucket():
    bucket_names = list()
    for each_bucket_info in s3_resource.buckets.all():
        print(each_bucket_info.name)
        bucket_names.append(each_bucket_info)
    return bucket_names
    
def download(bucket,video_folder):
    data_location = 's3://{}/{}'.format(bucket,video_folder)
    source = s3_resource.Bucket(name=data_location)
    
    for obj in source.objects.all():
        name = obj.name
        obj.Object.download_file(f'/home/sagemaker-user/opencv/stitching_video/{name}')
    
    
if __name__ == "__main__":
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    role = get_execution_role()

    bucket = 'tennisvideobucket/'
    m3 = '25-05-2020/3m'
    m35 = '25-05-2020/3m5'
    m4 = '25-05-20202/4m'
    folders = [m3,m35,m4]
#     access_bucket(bucket,folders[int(input("enter folder:[1/2/3]"))])
#     all_bucket()
#     download(bucket,folders[int(input("enter folder:[1/2/3]"))])