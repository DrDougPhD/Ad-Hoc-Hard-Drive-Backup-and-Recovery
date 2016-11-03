sed '/exclude_keyword/d' file
grep 'keyword' file
awk -F"\t" '{print $1}' backup_jazzpony.JPGs.txt > backup_jazzpony.JPGs.to_backup.txt

# Isolate file paths
awk -F"\t" '{print $1}' 

# Isolate file extensions
awk -F"." '{print $NF}' - 

# Histograph of file extensions
sort | uniq -c | awk '{print $2"\t"$1}' 

> backup_jazzpony.JPGs.to_backup.txt

sed '/exclude_keyword/d' file
grep 'keyword' file


############
# isolate filepaths | isolate filename | only print filenames with a period | isolate extension of filename | group extensions together | count unique extensions | sort by number of occurrences
awk -F"\t" '{print $1}' backup_jazzpony.txt | awk -F"/" '{print $NF}' - | sed -n '/\./p' - | awk -F"." '{print $NF}' - | sort | uniq -c | sort -gr | tee jazzpony_extension_histography.txt

############
# isolate filepaths | print only jpeg/JPEG files | remove any file in Music or AppData directory
awk -F"\t" '{print $1}' backup_jazzpony.txt | grep "\.JPG\|\.jpg\|\.JPEG\|\.jpeg" - | sed -e "/AppData\|Music/d"




sed -n '/\./p' sample.txt


# Isolate file paths
awk -F"\t" '{print $1}' 

# Isolate file extensions
awk -F"." '{print $NF}' - 

# Histograph of file extensions
sort | uniq -c | awk '{print $2"\t"$1}' 

> backup_jazzpony.JPGs.to_backup.txt
