#!/usr/bin/gawk -f

BEGIN{}
{
    res = match($0,/\[?(Ampere|Intel|AMD|NVIDIA).?.?.?(&reg;)?( \w+)?(-)?( Generation)?( (Altra|Xeon|EPYC|Epyc|Tesla|\w+)?.?(<sup>TM<\/sup>)?(&reg;)?(&trade;)?)? (\w+)(-)?(\w)*(])? (\w+)(-)?(\w)*(])?/,m)
    if ( res != 0 ){
        print "file= "ARGV[1]" res= "res" m= "m[0]
    }
}
END {}
