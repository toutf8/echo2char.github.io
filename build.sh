#!/bin/bash

action=$1

function build()
{
    hugo -d docs/
}

function dev()
{
    hugo serve
}

function main()
{
   if [ "$action" = "dev" ]; then
       dev
   else 
       if [ "$action" = "build" ]; then
           build
       fi
   fi
}

main
