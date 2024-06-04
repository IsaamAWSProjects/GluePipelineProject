# GluePipeline1

1. Creating the IAM roles:
   - Create a role for the code pipeline.
   - Set the use case case as EC2.
   - Attach the following policies: (AmazonS3FullAccess, AWSCloudFormationFullAccess, AWSCodeBuildAdminAccess, AWSCodePipeline_FullAccess, IAMFullAccess)
   - Edit the trust policy, and replace "ec2" with "codepipeline":
     
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}


|
|
v


{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "codepipeline.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
   - Create a role for the cloud formation.
   - Set the use case case as cloud formation. (Or can also edit the trust policy to select cloud formation?)
   - Attach the following policies: (AmazonS3FullAccess, IAMFullAccess, AWSGlueServiceRole, AWSCloudFormationFullAccess)

2. Create a S3 bucket.

3. Create 4 folders within the S3 bucket: (script, temp, input, output)
   -Upload the .csv file into the input folder.
   -Upload the Python script into the script folder (ensure the name of the bucket and the path to the folder are correct):


|
|
v

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data directly from S3
source_path = "s3://mycodepipelinebucket13/input/product_data.csv"
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": [source_path]},
    format_options={"withHeader": True}
)



# Convert to JSON format
json_path = "s3://mycodepipelinebucket13/output/target-data.json"
glueContext.write_dynamic_frame.from_options(
    frame=df,
    connection_type="s3",
    connection_options={"path": json_path},
    format="json"
)

job.commit()

5. Create a Github repository.
   
6. Create a new file in the repository, named "name".yml:


|
|
v

Resources:
  GlueJob:
    Type: AWS::Glue::Job
    Properties:
      Name: MyGlueJob  
      Role: !GetAtt GlueServiceRole.Arn
      Command:
        Name: glueetl
        ScriptLocation: s3://mycodepipelinebucket13/script/glue_script.py
      DefaultArguments:
        "--TempDir": "s3://mycodepipelinebucket13/temp/"
      GlueVersion: "2.0"
      WorkerType: G.1X
      NumberOfWorkers: 3


  GlueServiceRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-MyRoleForGlue"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: glue.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonS3FullAccess
        - arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole

        
7. Create a code pipeline.

8. Select a existing role within the pipeline, the code pipeline role created in step 1.

9. Select Github as the source for the pipeline.

10. Select the correct repository and branch containing the template file from step 6.

11. Select cloud formation for the deploy stage.

12. Select "Create or update stack" under "Action Mode".

13. Name the new stack.

14. Under "Artifact Name", select "Source Artifact" and input the name of the .yml file from step 6.

15. Under "Capabilities", select "CAPABILITY_NAMED_IAM".

16. Under "Role name", select the cloud formation role created in step 1.

17. Create the pipeline, it will automatically deploy.

18. Go to AWS Glue, the new Glue job should have been automatically created. It can now be run. 


