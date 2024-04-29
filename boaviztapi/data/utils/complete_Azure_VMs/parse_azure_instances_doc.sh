#!/bin/bash

# Documentation available at https://github.com/MicrosoftDocs/azure-docs
# Clone repo, then move to azure-docs/articles/virtual-machines

for i in $(ls azure-docs/articles/virtual-machines/*series.md)
do
  dos2unix "$i" 2>> /dev/null
  sed -e "s/\xe2\x80\xaf//g" "$i" > "tmp"
  #cat -A "$i" | sed 's#M-bM-^@M-/# #' | sed 's#M-BM-# #' > "tmp"
  cp "tmp" "$i"
  #comps=$(grep -PoE "\[?(Ampere|Intel|AMD|NVIDIA).?.?.?(&reg;)?( \w+)?(-)?( Generation)?( (Altra|Xeon|EPYC|Epyc|Tesla|\d\w+)?.?(<sup>TM<\/sup>)?(&reg;)?(&trade;)?)? (\w+)(-)?(\w)*]?" "$i");
  comps=$(gawk -f match_refs.awk "$i")
  name=$(echo "$i" | sed 's/-series\.md//')
  if [ ${#comps} -eq 0 ]
  then
    echo "$i : NOT FOUND !!!!!!!!!!!!!!!!!!!!!!!!!!!"
  fi
  comps=$(echo "$comps" | sort | uniq);
  echo $comps
  #echo "platform_azure_$name,Azure,,,,$comps",,,,,,,,,,,,,,, | tr -d "[" | sed 's/(&reg|®|™|<sup>TM<\/sup>)//' | sed 's/(&reg|®|™|<sup>TM<\/sup>)//';
done
