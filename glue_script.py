import sys
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize GlueContext and Job
glueContext = GlueContext(sc)
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Print a single statement
print("This is a testing output message.")

# Commit the job
job.commit()

