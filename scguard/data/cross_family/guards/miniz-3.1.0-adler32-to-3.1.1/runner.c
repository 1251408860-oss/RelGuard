#include <stdint.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8&&sizeof(uint32_t)==4,"ABI");
static uint32_t rf_left(uint32_t x,unsigned cfg,unsigned char*b){
(void)x;
if(cfg==0U){
uint32_t out=1U;
return out;}
if(cfg==1U){
uint32_t out=65537U;
out+=65537U*(uint32_t)b[0];
return out;}
if(cfg==2U){
uint32_t out=131073U;
out+=131073U*(uint32_t)b[0];
out+=65537U*(uint32_t)b[1];
return out;}
if(cfg==3U){
uint32_t out=196609U;
out+=196609U*(uint32_t)b[0];
out+=131073U*(uint32_t)b[1];
out+=65537U*(uint32_t)b[2];
return out;}
if(cfg==4U){
uint32_t out=262145U;
out+=262145U*(uint32_t)b[0];
out+=196609U*(uint32_t)b[1];
out+=131073U*(uint32_t)b[2];
out+=65537U*(uint32_t)b[3];
return out;}
if(cfg==5U){
uint32_t out=327681U;
out+=327681U*(uint32_t)b[0];
out+=262145U*(uint32_t)b[1];
out+=196609U*(uint32_t)b[2];
out+=131073U*(uint32_t)b[3];
out+=65537U*(uint32_t)b[4];
return out;}
if(cfg==6U){
uint32_t out=393217U;
out+=393217U*(uint32_t)b[0];
out+=327681U*(uint32_t)b[1];
out+=262145U*(uint32_t)b[2];
out+=196609U*(uint32_t)b[3];
out+=131073U*(uint32_t)b[4];
out+=65537U*(uint32_t)b[5];
return out;}
if(cfg==7U){
uint32_t out=458753U;
out+=458753U*(uint32_t)b[0];
out+=393217U*(uint32_t)b[1];
out+=327681U*(uint32_t)b[2];
out+=262145U*(uint32_t)b[3];
out+=196609U*(uint32_t)b[4];
out+=131073U*(uint32_t)b[5];
out+=65537U*(uint32_t)b[6];
return out;}
if(cfg==8U){
uint32_t out=524289U;
out+=524289U*(uint32_t)b[0];
out+=458753U*(uint32_t)b[1];
out+=393217U*(uint32_t)b[2];
out+=327681U*(uint32_t)b[3];
out+=262145U*(uint32_t)b[4];
out+=196609U*(uint32_t)b[5];
out+=131073U*(uint32_t)b[6];
out+=65537U*(uint32_t)b[7];
return out;}
return 0U;}
static uint32_t rf_right(uint32_t x,unsigned cfg,unsigned char*b){
(void)x;
if(cfg==0U){
uint32_t out=1U;
return out;}
if(cfg==1U){
uint32_t out=65537U;
out+=65537U*(uint32_t)b[0];
return out;}
if(cfg==2U){
uint32_t out=131073U;
out+=131073U*(uint32_t)b[0];
out+=65537U*(uint32_t)b[1];
return out;}
if(cfg==3U){
uint32_t out=196609U;
out+=196609U*(uint32_t)b[0];
out+=131073U*(uint32_t)b[1];
out+=65537U*(uint32_t)b[2];
return out;}
if(cfg==4U){
uint32_t out=262145U;
out+=262145U*(uint32_t)b[0];
out+=196609U*(uint32_t)b[1];
out+=131073U*(uint32_t)b[2];
out+=65537U*(uint32_t)b[3];
return out;}
if(cfg==5U){
uint32_t out=327681U;
out+=327681U*(uint32_t)b[0];
out+=262145U*(uint32_t)b[1];
out+=196609U*(uint32_t)b[2];
out+=131073U*(uint32_t)b[3];
out+=65537U*(uint32_t)b[4];
return out;}
if(cfg==6U){
uint32_t out=393217U;
out+=393217U*(uint32_t)b[0];
out+=327681U*(uint32_t)b[1];
out+=262145U*(uint32_t)b[2];
out+=196609U*(uint32_t)b[3];
out+=131073U*(uint32_t)b[4];
out+=65537U*(uint32_t)b[5];
return out;}
if(cfg==7U){
uint32_t out=458753U;
out+=458753U*(uint32_t)b[0];
out+=393217U*(uint32_t)b[1];
out+=327681U*(uint32_t)b[2];
out+=262145U*(uint32_t)b[3];
out+=196609U*(uint32_t)b[4];
out+=131073U*(uint32_t)b[5];
out+=65537U*(uint32_t)b[6];
return out;}
if(cfg==8U){
uint32_t out=524289U;
out+=524289U*(uint32_t)b[0];
out+=458753U*(uint32_t)b[1];
out+=393217U*(uint32_t)b[2];
out+=327681U*(uint32_t)b[3];
out+=262145U*(uint32_t)b[4];
out+=196609U*(uint32_t)b[5];
out+=131073U*(uint32_t)b[6];
out+=65537U*(uint32_t)b[7];
return out;}
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
