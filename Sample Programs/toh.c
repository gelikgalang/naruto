#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <limits.h>

int main()
{

    int disk=4;
    int src[disk],des[disk],aux[disk],temp[disk];
    int i=0,srcl,auxl,desl,total_num_of_moves=1,templ;
    while(disk>i)
    {
        src[i]=disk-i;
        i=i+1;
    }











    
    srcl=disk;
    auxl=0;
    desl=0;
    i=0;
    while(i<disk)
    {
        total_num_of_moves=total_num_of_moves*2;
        i=i+1;
    }
    total_num_of_moves= total_num_of_moves-1;













if(disk%2==1)
{

    for(i=1; i<=total_num_of_moves; i++)
    {
        if(i%3==1)
        {
            if(desl!=0)
                {
                    if(srcl!=0)
                    {
                        if(src[srcl-1]>des[desl-1])
                            {
                                src[srcl]=des[desl-1];
                                desl=desl-1;
                                srcl=srcl+1;
                                printf("Move disk destination to source\n");
                            }
                        else
                            {
                                des[desl]=src[srcl-1];
                                srcl=srcl-1;
                                desl=desl+1;
                                printf("Move disk source to destination\n");
                            }
                    }
                    else
                        {
                            src[0]=des[desl-1];
                            desl=desl-1;
                            srcl=srcl+1;
                            printf("Move disk destination to source\n");
                        }
                }
            else
                {
                    des[0]=src[srcl-1];
                    srcl=srcl-1;
                    desl=desl+1;
                    printf("Move disk source to destination\n");
                }
        }
        else if(i%3==2)
        {
            if(auxl!=0)
                {
                    if(srcl!=0)
                    {
                        if(src[srcl-1]>aux[auxl-1])
                            {
                                src[srcl]=aux[auxl-1];
                                auxl=auxl-1;
                                srcl=srcl+1;
                                printf("Move disk auxiliary to source\n");
                            }
                        else
                            {
                                aux[auxl]=src[srcl-1];
                                srcl=srcl-1;
                                auxl=auxl+1;
                                printf("Move disk source to auxiliary\n");
                            }
                    }
                    else
                        {
                            src[0]=aux[auxl-1];
                            auxl=auxl-1;
                            srcl=srcl+1;
                            printf("Move disk auxiliary to source\n");
                        }
                }
            else
                {
                    aux[0]=src[srcl-1];
                    srcl=srcl-1;
                    auxl=auxl+1;
                    printf("Move disk source to auxiliary\n");
                }
        }
        else if(i%3==0)
        {
            if(auxl!=0)
                {
                    if(desl!=0)
                    {
                        if(des[desl-1]>aux[auxl-1])
                            {
                                des[desl]=aux[auxl-1];
                                auxl=auxl-1;
                                desl=desl+1;
                                printf("Move disk auxiliary to destination\n");
                            }
                        else
                            {
                                aux[auxl]=des[desl-1];
                                desl=desl-1;
                                auxl=auxl+1;
                                printf("Move disk destination to auxiliary\n");
                            }
                    }
                    else
                        {
                            des[0]=aux[auxl-1];
                            auxl=auxl-1;
                            desl=desl+1;
                            printf("Move disk auxiliary to destination\n");
                        }
                }
            else
                {
                    aux[0]=des[desl-1];
                    desl=desl-1;
                    auxl=auxl+1;
                    printf("Move disk destination to auxiliary\n");
                }
        }
        
    }
}

else
{

    for(i=1; i<=total_num_of_moves; i++)
    {
        if(i%3==1)
        {
            if(auxl!=0)
                {
                    if(srcl!=0)
                    {
                        if(src[srcl-1]>aux[auxl-1])
                            {
                                src[srcl]=aux[auxl-1];
                                auxl=auxl-1;
                                srcl=srcl+1;
                                printf("Move disk auxiliary to source\n");
                            }
                        else
                            {
                                aux[auxl]=src[srcl-1];
                                srcl=srcl-1;
                                auxl=auxl+1;
                                printf("Move disk source to auxiliary\n");
                            }
                    }
                    else
                        {
                            src[0]=aux[auxl-1];
                            auxl=auxl-1;
                            srcl=srcl+1;
                            printf("Move disk auxiliary to source\n");
                        }
                }
            else
                {
                    aux[0]=src[srcl-1];
                    srcl=srcl-1;
                    auxl=auxl+1;
                    printf("Move disk source to auxiliary\n");
                }
        }
        else if(i%3==2)
        {
            if(desl!=0)
                {
                    if(srcl!=0)
                    {
                        if(src[srcl-1]>des[desl-1])
                            {
                                src[srcl]=des[desl-1];
                                desl=desl-1;
                                srcl=srcl+1;
                                printf("Move disk destination to source\n");
                            }
                        else
                            {
                                des[desl]=src[srcl-1];
                                srcl=srcl-1;
                                desl=desl+1;
                                printf("Move disk source to destination\n");
                            }
                    }
                    else
                        {
                            src[0]=des[desl-1];
                            desl=desl-1;
                            srcl=srcl+1;
                            printf("Move disk destination to source\n");
                        }
                }
            else
                {
                    des[0]=src[srcl-1];
                    srcl=srcl-1;
                    desl=desl+1;
                    printf("Move disk source to destination\n");
                }
        }
        else if(i%3==0)
        {
            if(desl!=0)
                {
                    if(auxl!=0)
                    {
                        if(aux[auxl-1]>des[desl-1])
                            {
                                aux[auxl]=des[desl-1];
                                desl=desl-1;
                                auxl=auxl+1;
                                printf("Move disk destination to auxiliary\n");
                            }
                        else
                            {
                                des[desl]=aux[auxl-1];
                                auxl=auxl-1;
                                desl=desl+1;
                                printf("Move disk auxiliary to destination\n");
                            }
                    }
                    else
                        {
                            aux[0]=des[desl-1];
                            desl=desl-1;
                            auxl=auxl+1;
                            printf("Move disk destination to auxiliary\n");
                        }
                }
            else
                {
                    des[0]=aux[auxl-1];
                    auxl=auxl-1;
                    desl=desl+1;
                    printf("Move disk auxiliary to destination\n");
                }
        }
        
    }
}


    printf("%d\n%d\n%d\n",srcl,auxl,desl );
    i=0;
    while(i<desl){
        printf("%d   ",des[i] );
        i=i+1;
    }
}