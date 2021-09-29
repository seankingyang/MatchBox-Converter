pyinstaller="/Users/IsaacYang/miniconda3/envs/new1/bin/pyinstaller"

project_path=$(cd "$(dirname "$0")"; pwd)

echo "-----------$project_path--------"
cd $project_path
echo "------- Now PWD:`pwd` -------"
py_spec="$project_path/MatchBox+MasterPlanConverterUI.spec"
rm -rf build dist __pycache__ Release

`$pyinstaller $py_spec`
mkdir "$project_path/Release/"
cp -rf "$project_path/dist/MatchBox+ MasterPlan Converter UI.app" "$project_path/Release/MatchBox+ MasterPlan Converter UI.app" 
sleep 1
cd "$project_path/Release/"
zip -r "MatchBox+ MasterPlan Converter UI.zip" "MatchBox+ MasterPlan Converter UI.app"
cd $project_path
cp -rf "$project_path/Data/Assets" "$project_path/Release/"
cp -f "$project_path/make_COV_UI.sh" "$project_path/make_COV_UI"
chmod +x "$project_path/make_COV_UI"




