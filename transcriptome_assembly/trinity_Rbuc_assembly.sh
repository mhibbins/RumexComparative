#!/bin/bash

cd /ohta1/mark.hibbins/Assemblies/Trinity/

parallel --jobs 2 < Trinity_jobs_bucephalophorus.txt > Trinity_jobs_bucephalophorus.out 2> Trinity_jobs_bucephalophorus.err

