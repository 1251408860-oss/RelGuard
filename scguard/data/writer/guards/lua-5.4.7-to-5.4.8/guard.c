/* Source identities and premises are in binding.json. Return 0 UNKNOWN,
1 EQUAL, 2 UNEQUAL. Caller supplies valid readable eight-byte entry arrays. */
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8 && sizeof(unsigned)==4 && sizeof(int)==4,"ABI");
static int bg_old(unsigned x,unsigned cap,unsigned char *dst){
if(cap==8U){
if(x<=127U){
{unsigned initial=dst[7];dst[7]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[6];dst[6]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[7];dst[7]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=65535U){
{unsigned initial=dst[5];dst[5]=(unsigned char)(224U|((x>>12U)&15U));}
{unsigned initial=dst[6];dst[6]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[7];dst[7]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=1114111U){
{unsigned initial=dst[4];dst[4]=(unsigned char)(240U|((x>>18U)&7U));}
{unsigned initial=dst[5];dst[5]=(unsigned char)(128U|((x>>12U)&63U));}
{unsigned initial=dst[6];dst[6]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[7];dst[7]=(unsigned char)(128U|(x&63U));}
return 4;}
}
return 0;}
static int bg_new(unsigned x,unsigned cap,unsigned char *dst){
if(cap==8U){
if(x<=127U){
{unsigned initial=dst[7];dst[7]=(unsigned char)((x&127U));}
return 1;}
if(x<=2047U){
{unsigned initial=dst[6];dst[6]=(unsigned char)(192U|((x>>6U)&31U));}
{unsigned initial=dst[7];dst[7]=(unsigned char)(128U|(x&63U));}
return 2;}
if(x<=65535U){
{unsigned initial=dst[5];dst[5]=(unsigned char)(224U|((x>>12U)&15U));}
{unsigned initial=dst[6];dst[6]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[7];dst[7]=(unsigned char)(128U|(x&63U));}
return 3;}
if(x<=1114111U){
{unsigned initial=dst[4];dst[4]=(unsigned char)(240U|((x>>18U)&7U));}
{unsigned initial=dst[5];dst[5]=(unsigned char)(128U|((x>>12U)&63U));}
{unsigned initial=dst[6];dst[6]=(unsigned char)(128U|((x>>6U)&63U));}
{unsigned initial=dst[7];dst[7]=(unsigned char)(128U|(x&63U));}
return 4;}
}
return 0;}

int bg_decide(unsigned xa,unsigned ca,const unsigned char *ea,
              unsigned xb,unsigned cb,const unsigned char *eb,unsigned mask){
 if(!ea||!eb||xa>1114111U||xb>1114111U||!mask||mask>511U||!(ca==8U)||!(cb==8U))return 0;
 unsigned char a[8],b[8];for(unsigned i=0;i<8;i++){a[i]=ea[i];b[i]=eb[i];}
 int ra=bg_old(xa,ca,a),rb=bg_new(xb,cb,b);
 if((mask&1U)&&ra!=rb)return 2;
 for(unsigned i=0;i<8;i++)if((mask&(2U<<i))&&a[i]!=b[i])return 2;
 return 1;
}
