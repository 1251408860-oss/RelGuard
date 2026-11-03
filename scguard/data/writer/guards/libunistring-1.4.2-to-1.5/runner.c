/* Source identities and premises are in binding.json. Return 0 UNKNOWN,
1 EQUAL, 2 UNEQUAL. Caller supplies valid readable eight-byte entry arrays. */
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8 && sizeof(unsigned)==4 && sizeof(int)==4,"ABI");
static int bg_old(unsigned x,unsigned cap,unsigned char *dst){
if(cap==0U){
if(x<=55295U){
return -2;}
if(x<=57343U){
return -1;}
if(x<=1114111U){
return -2;}
}
if(cap==1U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=55295U){
return -2;}
if(x<=57343U){
return -1;}
if(x<=1114111U){
return -2;}
}
if(cap==2U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=55295U){
return -2;}
if(x<=57343U){
return -1;}
if(x<=1114111U){
return -2;}
}
if(cap==3U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=55295U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(224U|((x>>12U)&15U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=57343U){
return -1;}
if(x<=65535U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(238U|((x>>12U)&1U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=1114111U){
return -2;}
}
if(cap==4U||cap==5U||cap==6U||cap==7U||cap==8U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=55295U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(224U|((x>>12U)&15U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=57343U){
return -1;}
if(x<=65535U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(238U|((x>>12U)&1U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=1114111U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(240U|((x>>18U)&7U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>12U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[3];dst[3]=(unsigned char)(128U|(x&63U));}
return 4;}
}
return 0;}
static int bg_new(unsigned x,unsigned cap,unsigned char *dst){
if(cap==0U){
if(x<=55295U){
return -2;}
if(x<=57343U){
return -1;}
if(x<=1114111U){
return -2;}
}
if(cap==1U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=55295U){
return -2;}
if(x<=57343U){
return -1;}
if(x<=1114111U){
return -2;}
}
if(cap==2U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=55295U){
return -2;}
if(x<=57343U){
return -1;}
if(x<=1114111U){
return -2;}
}
if(cap==3U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=55295U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(224U|((x>>12U)&15U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=57343U){
return -1;}
if(x<=65535U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(238U|((x>>12U)&1U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=1114111U){
return -2;}
}
if(cap==4U||cap==5U||cap==6U||cap==7U||cap==8U){
if(x<=127U){
{unsigned initial=dst[0];dst[0]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=55295U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(224U|((x>>12U)&15U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=57343U){
return -1;}
if(x<=65535U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(238U|((x>>12U)&1U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=1114111U){
{unsigned initial=dst[0];dst[0]=(unsigned char)(240U|((x>>18U)&7U));}
{unsigned initial=dst[1];dst[1]=(unsigned char)(128U|((x>>12U)&63U));}
{unsigned initial=dst[2];dst[2]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[3];dst[3]=(unsigned char)(128U|(x&63U));}
return 4;}
}
return 0;}

int bg_decide(unsigned xa,unsigned ca,const unsigned char *ea,
              unsigned xb,unsigned cb,const unsigned char *eb,unsigned mask){
 if(!ea||!eb||xa>1114111U||xb>1114111U||!mask||mask>511U||!(ca==0U||ca==1U||ca==2U||ca==3U||ca==4U||ca==5U||ca==6U||ca==7U||ca==8U)||!(cb==0U||cb==1U||cb==2U||cb==3U||cb==4U||cb==5U||cb==6U||cb==7U||cb==8U))return 0;
 unsigned char a[8],b[8];for(unsigned i=0;i<8;i++){a[i]=ea[i];b[i]=eb[i];}
 int ra=bg_old(xa,ca,a),rb=bg_new(xb,cb,b);
 if((mask&1U)&&ra!=rb)return 2;
 for(unsigned i=0;i<8;i++)if((mask&(2U<<i))&&a[i]!=b[i])return 2;
 return 1;
}

#include <stdio.h>
int main(void){uint32_t xa,ca,xb,cb,mask;unsigned char a[8],b[8];
while(fread(&xa,4,1,stdin)==1){
 if(fread(&ca,4,1,stdin)!=1||fread(a,8,1,stdin)!=1||fread(&xb,4,1,stdin)!=1||fread(&cb,4,1,stdin)!=1||fread(b,8,1,stdin)!=1||fread(&mask,4,1,stdin)!=1)return 3;
 unsigned char answer=(unsigned char)bg_decide(xa,ca,a,xb,cb,b,mask);if(fwrite(&answer,1,1,stdout)!=1)return 4;
}return ferror(stdin)?5:0;}
