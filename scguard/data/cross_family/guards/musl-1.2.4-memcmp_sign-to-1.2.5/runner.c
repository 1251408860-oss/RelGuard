#include <stdint.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8&&sizeof(uint32_t)==4,"ABI");
static uint32_t rf_left(uint32_t x,unsigned cfg,unsigned char*b){
(void)x;
if(cfg==0U){
return 0U;}
if(cfg==1U){
if(b[0]!=b[4]){if(b[0]<b[4])return UINT32_MAX;return 1U;}
if(b[1]!=b[5]){if(b[1]<b[5])return UINT32_MAX;return 1U;}
if(b[2]!=b[6]){if(b[2]<b[6])return UINT32_MAX;return 1U;}
if(b[3]!=b[7]){if(b[3]<b[7])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==2U){
if(b[4]!=b[0]){if(b[4]<b[0])return UINT32_MAX;return 1U;}
if(b[5]!=b[1]){if(b[5]<b[1])return UINT32_MAX;return 1U;}
if(b[6]!=b[2]){if(b[6]<b[2])return UINT32_MAX;return 1U;}
if(b[7]!=b[3]){if(b[7]<b[3])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==3U){
if(b[0]!=b[2]){if(b[0]<b[2])return UINT32_MAX;return 1U;}
if(b[1]!=b[3]){if(b[1]<b[3])return UINT32_MAX;return 1U;}
if(b[0]!=b[4]){if(b[0]<b[4])return UINT32_MAX;return 1U;}
if(b[1]!=b[5]){if(b[1]<b[5])return UINT32_MAX;return 1U;}
if(b[0]!=b[6]){if(b[0]<b[6])return UINT32_MAX;return 1U;}
if(b[1]!=b[7]){if(b[1]<b[7])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==4U){
if(b[2]!=b[0]){if(b[2]<b[0])return UINT32_MAX;return 1U;}
if(b[3]!=b[1]){if(b[3]<b[1])return UINT32_MAX;return 1U;}
if(b[4]!=b[0]){if(b[4]<b[0])return UINT32_MAX;return 1U;}
if(b[5]!=b[1]){if(b[5]<b[1])return UINT32_MAX;return 1U;}
if(b[6]!=b[0]){if(b[6]<b[0])return UINT32_MAX;return 1U;}
if(b[7]!=b[1]){if(b[7]<b[1])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==5U){
return 0U;}
if(cfg==6U){
if(b[3]!=b[4]){if(b[3]<b[4])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==7U){
if(b[1]!=b[2]){if(b[1]<b[2])return UINT32_MAX;return 1U;}
if(b[1]!=b[3]){if(b[1]<b[3])return UINT32_MAX;return 1U;}
if(b[1]!=b[4]){if(b[1]<b[4])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==8U){
if(b[2]!=b[1]){if(b[2]<b[1])return UINT32_MAX;return 1U;}
if(b[3]!=b[1]){if(b[3]<b[1])return UINT32_MAX;return 1U;}
if(b[4]!=b[1]){if(b[4]<b[1])return UINT32_MAX;return 1U;}
return 0U;}
return 0U;}
static uint32_t rf_right(uint32_t x,unsigned cfg,unsigned char*b){
(void)x;
if(cfg==0U){
return 0U;}
if(cfg==1U){
if(b[0]!=b[4]){if(b[0]<b[4])return UINT32_MAX;return 1U;}
if(b[1]!=b[5]){if(b[1]<b[5])return UINT32_MAX;return 1U;}
if(b[2]!=b[6]){if(b[2]<b[6])return UINT32_MAX;return 1U;}
if(b[3]!=b[7]){if(b[3]<b[7])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==2U){
if(b[4]!=b[0]){if(b[4]<b[0])return UINT32_MAX;return 1U;}
if(b[5]!=b[1]){if(b[5]<b[1])return UINT32_MAX;return 1U;}
if(b[6]!=b[2]){if(b[6]<b[2])return UINT32_MAX;return 1U;}
if(b[7]!=b[3]){if(b[7]<b[3])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==3U){
if(b[0]!=b[2]){if(b[0]<b[2])return UINT32_MAX;return 1U;}
if(b[1]!=b[3]){if(b[1]<b[3])return UINT32_MAX;return 1U;}
if(b[0]!=b[4]){if(b[0]<b[4])return UINT32_MAX;return 1U;}
if(b[1]!=b[5]){if(b[1]<b[5])return UINT32_MAX;return 1U;}
if(b[0]!=b[6]){if(b[0]<b[6])return UINT32_MAX;return 1U;}
if(b[1]!=b[7]){if(b[1]<b[7])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==4U){
if(b[2]!=b[0]){if(b[2]<b[0])return UINT32_MAX;return 1U;}
if(b[3]!=b[1]){if(b[3]<b[1])return UINT32_MAX;return 1U;}
if(b[4]!=b[0]){if(b[4]<b[0])return UINT32_MAX;return 1U;}
if(b[5]!=b[1]){if(b[5]<b[1])return UINT32_MAX;return 1U;}
if(b[6]!=b[0]){if(b[6]<b[0])return UINT32_MAX;return 1U;}
if(b[7]!=b[1]){if(b[7]<b[1])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==5U){
return 0U;}
if(cfg==6U){
if(b[3]!=b[4]){if(b[3]<b[4])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==7U){
if(b[1]!=b[2]){if(b[1]<b[2])return UINT32_MAX;return 1U;}
if(b[1]!=b[3]){if(b[1]<b[3])return UINT32_MAX;return 1U;}
if(b[1]!=b[4]){if(b[1]<b[4])return UINT32_MAX;return 1U;}
return 0U;}
if(cfg==8U){
if(b[2]!=b[1]){if(b[2]<b[1])return UINT32_MAX;return 1U;}
if(b[3]!=b[1]){if(b[3]<b[1])return UINT32_MAX;return 1U;}
if(b[4]!=b[1]){if(b[4]<b[1])return UINT32_MAX;return 1U;}
return 0U;}
return 0U;}
int af_guard(uint32_t xa,unsigned ca,const unsigned char*a,uint32_t xb,unsigned cb,const unsigned char*b,unsigned obs){
if(!a||!b||ca>8U||cb>8U||obs>4U)return 0;
unsigned char left[8],right[8];for(unsigned i=0;i<8;i++){left[i]=a[i];right[i]=b[i];}
uint32_t ra=rf_left(xa,ca,left),rb=rf_right(xb,cb,right);int equal=1;
if(obs==0U||obs==4U)equal=ra==rb;
unsigned start=obs==2U?4U:0U,end=obs==1U?4U:8U;
if(obs!=0U)for(unsigned i=start;i<end;i++)if(left[i]!=right[i])equal=0;
return equal?1:2;}

#include <stdio.h>
int main(void){uint32_t xa,ca,xb,cb,obs;unsigned char a[8],b[8];
while(fread(&xa,4,1,stdin)==1){if(fread(&ca,4,1,stdin)!=1||fread(a,8,1,stdin)!=1||fread(&xb,4,1,stdin)!=1||fread(&cb,4,1,stdin)!=1||fread(b,8,1,stdin)!=1||fread(&obs,4,1,stdin)!=1)return 3;
unsigned char v=(unsigned char)af_guard(xa,ca,a,xb,cb,b,obs);if(fwrite(&v,1,1,stdout)!=1)return 4;
}return ferror(stdin)?5:0;}
