# for i in `cat err`; do
# 	 aws s3 cp --profile moc s3://thoth/data/zero-prod/adviser/$i.request errs/$i.request
# 	 aws s3 cp --profile moc s3://thoth/data/zero-prod/adviser/$i errs/$i
#  done

for i in `cat err`; do
    # mkdir -p e_inputs/$i
    # cat errs/$i | jq .result.parameters.project.requirements > e_inputs/$i/Pipfile
    # rt=`cat errs/$i | jq .result.parameters.recommendation_type | tr -d \"`
    # touch e_inputs/$i/$rt
    # cat errs/$i | jq .result.parameters.project.runtime_environment > e_inputs/$i/runtime_environment.json
    echo ">>>> $i"
    cat e_inputs/$i/runtime_environment.json | jq .operating_system
    cat e_inputs/$i/runtime_environment.json | jq .python_version
done

