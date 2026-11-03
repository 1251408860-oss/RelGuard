#include <stdint.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8&&sizeof(uint32_t)==4,"ABI");
static unsigned af_parity(uint32_t v){
v^=v>>16;v^=v>>8;v^=v>>4;return (0x6996U>>(v&15U))&1U;}

static uint32_t rf_left(uint32_t x,unsigned cfg,unsigned char *b){
uint32_t w0=x,w1=0,w2=0;
for(unsigned i=0;i<4;i++){w1|=(uint32_t)b[i]<<(8U*i);w2|=(uint32_t)b[i+4]<<(8U*i);}

if(cfg==0U){
uint32_t o0=0U;
uint32_t o1=w1;
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==1U){
uint32_t o0=((1U)<<2U);
uint32_t o1=w1;
uint32_t o2=w1;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==2U){
uint32_t o0=0U;
uint32_t o1=w2;
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==3U){
uint32_t o0=((1U)<<1U);
uint32_t o1=((((w1>>0U)&1U))<<0U)|((((w1>>1U)&1U))<<1U)|((((w1>>2U)&1U))<<2U)|((((w1>>3U)&1U))<<3U)|((((w1>>4U)&1U))<<4U)|((((w1>>5U)&1U))<<5U)|((((w1>>6U)&1U))<<6U)|((((w1>>7U)&1U))<<7U)|((((w1>>8U)&1U))<<8U)|((((w1>>9U)&1U))<<9U)|((((w1>>10U)&1U))<<10U)|((((w1>>11U)&1U))<<11U)|((((w1>>12U)&1U))<<12U)|((((w1>>13U)&1U))<<13U)|((((w1>>14U)&1U))<<14U)|((((w1>>15U)&1U))<<15U)|((((w1>>0U)&1U))<<16U)|((((w1>>1U)&1U))<<17U)|((((w1>>2U)&1U))<<18U)|((((w1>>3U)&1U))<<19U)|((((w1>>4U)&1U))<<20U)|((((w1>>5U)&1U))<<21U)|((((w1>>6U)&1U))<<22U)|((((w1>>7U)&1U))<<23U)|((((w1>>8U)&1U))<<24U)|((((w1>>9U)&1U))<<25U)|((((w1>>10U)&1U))<<26U)|((((w1>>11U)&1U))<<27U)|((((w1>>12U)&1U))<<28U)|((((w1>>13U)&1U))<<29U)|((((w1>>14U)&1U))<<30U)|((((w1>>15U)&1U))<<31U);
uint32_t o2=((((w1>>16U)&1U))<<0U)|((((w1>>17U)&1U))<<1U)|((((w1>>18U)&1U))<<2U)|((((w1>>19U)&1U))<<3U)|((((w1>>20U)&1U))<<4U)|((((w1>>21U)&1U))<<5U)|((((w1>>22U)&1U))<<6U)|((((w1>>23U)&1U))<<7U)|((((w1>>24U)&1U))<<8U)|((((w1>>25U)&1U))<<9U)|((((w1>>26U)&1U))<<10U)|((((w1>>27U)&1U))<<11U)|((((w1>>28U)&1U))<<12U)|((((w1>>29U)&1U))<<13U)|((((w1>>30U)&1U))<<14U)|((((w1>>31U)&1U))<<15U)|((((w2>>0U)&1U))<<16U)|((((w2>>1U)&1U))<<17U)|((((w2>>2U)&1U))<<18U)|((((w2>>3U)&1U))<<19U)|((((w2>>4U)&1U))<<20U)|((((w2>>5U)&1U))<<21U)|((((w2>>6U)&1U))<<22U)|((((w2>>7U)&1U))<<23U)|((((w2>>8U)&1U))<<24U)|((((w2>>9U)&1U))<<25U)|((((w2>>10U)&1U))<<26U)|((((w2>>11U)&1U))<<27U)|((((w2>>12U)&1U))<<28U)|((((w2>>13U)&1U))<<29U)|((((w2>>14U)&1U))<<30U)|((((w2>>15U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==4U){
uint32_t o0=0U;
uint32_t o1=((((w1>>16U)&1U))<<0U)|((((w1>>17U)&1U))<<1U)|((((w1>>18U)&1U))<<2U)|((((w1>>19U)&1U))<<3U)|((((w1>>20U)&1U))<<4U)|((((w1>>21U)&1U))<<5U)|((((w1>>22U)&1U))<<6U)|((((w1>>23U)&1U))<<7U)|((((w1>>24U)&1U))<<8U)|((((w1>>25U)&1U))<<9U)|((((w1>>26U)&1U))<<10U)|((((w1>>27U)&1U))<<11U)|((((w1>>28U)&1U))<<12U)|((((w1>>29U)&1U))<<13U)|((((w1>>30U)&1U))<<14U)|((((w1>>31U)&1U))<<15U)|((((w2>>0U)&1U))<<16U)|((((w2>>1U)&1U))<<17U)|((((w2>>2U)&1U))<<18U)|((((w2>>3U)&1U))<<19U)|((((w2>>4U)&1U))<<20U)|((((w2>>5U)&1U))<<21U)|((((w2>>6U)&1U))<<22U)|((((w2>>7U)&1U))<<23U)|((((w2>>8U)&1U))<<24U)|((((w2>>9U)&1U))<<25U)|((((w2>>10U)&1U))<<26U)|((((w2>>11U)&1U))<<27U)|((((w2>>12U)&1U))<<28U)|((((w2>>13U)&1U))<<29U)|((((w2>>14U)&1U))<<30U)|((((w2>>15U)&1U))<<31U);
uint32_t o2=((((w2>>16U)&1U))<<0U)|((((w2>>17U)&1U))<<1U)|((((w2>>18U)&1U))<<2U)|((((w2>>19U)&1U))<<3U)|((((w2>>20U)&1U))<<4U)|((((w2>>21U)&1U))<<5U)|((((w2>>22U)&1U))<<6U)|((((w2>>23U)&1U))<<7U)|((((w2>>24U)&1U))<<8U)|((((w2>>25U)&1U))<<9U)|((((w2>>26U)&1U))<<10U)|((((w2>>27U)&1U))<<11U)|((((w2>>28U)&1U))<<12U)|((((w2>>29U)&1U))<<13U)|((((w2>>30U)&1U))<<14U)|((((w2>>31U)&1U))<<15U)|((((w2>>16U)&1U))<<16U)|((((w2>>17U)&1U))<<17U)|((((w2>>18U)&1U))<<18U)|((((w2>>19U)&1U))<<19U)|((((w2>>20U)&1U))<<20U)|((((w2>>21U)&1U))<<21U)|((((w2>>22U)&1U))<<22U)|((((w2>>23U)&1U))<<23U)|((((w2>>24U)&1U))<<24U)|((((w2>>25U)&1U))<<25U)|((((w2>>26U)&1U))<<26U)|((((w2>>27U)&1U))<<27U)|((((w2>>28U)&1U))<<28U)|((((w2>>29U)&1U))<<29U)|((((w2>>30U)&1U))<<30U)|((((w2>>31U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==5U){
uint32_t o0=0U;
uint32_t o1=w1;
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==6U){
uint32_t o0=((1U)<<2U);
uint32_t o1=w1;
uint32_t o2=((((w1>>24U)&1U))<<0U)|((((w1>>25U)&1U))<<1U)|((((w1>>26U)&1U))<<2U)|((((w1>>27U)&1U))<<3U)|((((w1>>28U)&1U))<<4U)|((((w1>>29U)&1U))<<5U)|((((w1>>30U)&1U))<<6U)|((((w1>>31U)&1U))<<7U)|((((w2>>8U)&1U))<<8U)|((((w2>>9U)&1U))<<9U)|((((w2>>10U)&1U))<<10U)|((((w2>>11U)&1U))<<11U)|((((w2>>12U)&1U))<<12U)|((((w2>>13U)&1U))<<13U)|((((w2>>14U)&1U))<<14U)|((((w2>>15U)&1U))<<15U)|((((w2>>16U)&1U))<<16U)|((((w2>>17U)&1U))<<17U)|((((w2>>18U)&1U))<<18U)|((((w2>>19U)&1U))<<19U)|((((w2>>20U)&1U))<<20U)|((((w2>>21U)&1U))<<21U)|((((w2>>22U)&1U))<<22U)|((((w2>>23U)&1U))<<23U)|((((w2>>24U)&1U))<<24U)|((((w2>>25U)&1U))<<25U)|((((w2>>26U)&1U))<<26U)|((((w2>>27U)&1U))<<27U)|((((w2>>28U)&1U))<<28U)|((((w2>>29U)&1U))<<29U)|((((w2>>30U)&1U))<<30U)|((((w2>>31U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==7U){
uint32_t o0=((1U)<<1U);
uint32_t o1=((((w1>>0U)&1U))<<0U)|((((w1>>1U)&1U))<<1U)|((((w1>>2U)&1U))<<2U)|((((w1>>3U)&1U))<<3U)|((((w1>>4U)&1U))<<4U)|((((w1>>5U)&1U))<<5U)|((((w1>>6U)&1U))<<6U)|((((w1>>7U)&1U))<<7U)|((((w1>>8U)&1U))<<8U)|((((w1>>9U)&1U))<<9U)|((((w1>>10U)&1U))<<10U)|((((w1>>11U)&1U))<<11U)|((((w1>>12U)&1U))<<12U)|((((w1>>13U)&1U))<<13U)|((((w1>>14U)&1U))<<14U)|((((w1>>15U)&1U))<<15U)|((((w1>>8U)&1U))<<16U)|((((w1>>9U)&1U))<<17U)|((((w1>>10U)&1U))<<18U)|((((w1>>11U)&1U))<<19U)|((((w1>>12U)&1U))<<20U)|((((w1>>13U)&1U))<<21U)|((((w1>>14U)&1U))<<22U)|((((w1>>15U)&1U))<<23U)|((((w1>>16U)&1U))<<24U)|((((w1>>17U)&1U))<<25U)|((((w1>>18U)&1U))<<26U)|((((w1>>19U)&1U))<<27U)|((((w1>>20U)&1U))<<28U)|((((w1>>21U)&1U))<<29U)|((((w1>>22U)&1U))<<30U)|((((w1>>23U)&1U))<<31U);
uint32_t o2=((((w1>>24U)&1U))<<0U)|((((w1>>25U)&1U))<<1U)|((((w1>>26U)&1U))<<2U)|((((w1>>27U)&1U))<<3U)|((((w1>>28U)&1U))<<4U)|((((w1>>29U)&1U))<<5U)|((((w1>>30U)&1U))<<6U)|((((w1>>31U)&1U))<<7U)|((((w2>>8U)&1U))<<8U)|((((w2>>9U)&1U))<<9U)|((((w2>>10U)&1U))<<10U)|((((w2>>11U)&1U))<<11U)|((((w2>>12U)&1U))<<12U)|((((w2>>13U)&1U))<<13U)|((((w2>>14U)&1U))<<14U)|((((w2>>15U)&1U))<<15U)|((((w2>>16U)&1U))<<16U)|((((w2>>17U)&1U))<<17U)|((((w2>>18U)&1U))<<18U)|((((w2>>19U)&1U))<<19U)|((((w2>>20U)&1U))<<20U)|((((w2>>21U)&1U))<<21U)|((((w2>>22U)&1U))<<22U)|((((w2>>23U)&1U))<<23U)|((((w2>>24U)&1U))<<24U)|((((w2>>25U)&1U))<<25U)|((((w2>>26U)&1U))<<26U)|((((w2>>27U)&1U))<<27U)|((((w2>>28U)&1U))<<28U)|((((w2>>29U)&1U))<<29U)|((((w2>>30U)&1U))<<30U)|((((w2>>31U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==8U){
uint32_t o0=((1U)<<0U);
uint32_t o1=((((w1>>0U)&1U))<<0U)|((((w1>>1U)&1U))<<1U)|((((w1>>2U)&1U))<<2U)|((((w1>>3U)&1U))<<3U)|((((w1>>4U)&1U))<<4U)|((((w1>>5U)&1U))<<5U)|((((w1>>6U)&1U))<<6U)|((((w1>>7U)&1U))<<7U)|((((w1>>16U)&1U))<<8U)|((((w1>>17U)&1U))<<9U)|((((w1>>18U)&1U))<<10U)|((((w1>>19U)&1U))<<11U)|((((w1>>20U)&1U))<<12U)|((((w1>>21U)&1U))<<13U)|((((w1>>22U)&1U))<<14U)|((((w1>>23U)&1U))<<15U)|((((w1>>24U)&1U))<<16U)|((((w1>>25U)&1U))<<17U)|((((w1>>26U)&1U))<<18U)|((((w1>>27U)&1U))<<19U)|((((w1>>28U)&1U))<<20U)|((((w1>>29U)&1U))<<21U)|((((w1>>30U)&1U))<<22U)|((((w1>>31U)&1U))<<23U)|((((w2>>0U)&1U))<<24U)|((((w2>>1U)&1U))<<25U)|((((w2>>2U)&1U))<<26U)|((((w2>>3U)&1U))<<27U)|((((w2>>4U)&1U))<<28U)|((((w2>>5U)&1U))<<29U)|((((w2>>6U)&1U))<<30U)|((((w2>>7U)&1U))<<31U);
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
return 0U;}
static uint32_t rf_right(uint32_t x,unsigned cfg,unsigned char *b){
uint32_t w0=x,w1=0,w2=0;
for(unsigned i=0;i<4;i++){w1|=(uint32_t)b[i]<<(8U*i);w2|=(uint32_t)b[i+4]<<(8U*i);}

if(cfg==0U){
uint32_t o0=0U;
uint32_t o1=w1;
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==1U){
uint32_t o0=((1U)<<2U);
uint32_t o1=w1;
uint32_t o2=w1;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==2U){
uint32_t o0=0U;
uint32_t o1=w2;
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==3U){
uint32_t o0=((1U)<<1U);
uint32_t o1=((((w1>>0U)&1U))<<0U)|((((w1>>1U)&1U))<<1U)|((((w1>>2U)&1U))<<2U)|((((w1>>3U)&1U))<<3U)|((((w1>>4U)&1U))<<4U)|((((w1>>5U)&1U))<<5U)|((((w1>>6U)&1U))<<6U)|((((w1>>7U)&1U))<<7U)|((((w1>>8U)&1U))<<8U)|((((w1>>9U)&1U))<<9U)|((((w1>>10U)&1U))<<10U)|((((w1>>11U)&1U))<<11U)|((((w1>>12U)&1U))<<12U)|((((w1>>13U)&1U))<<13U)|((((w1>>14U)&1U))<<14U)|((((w1>>15U)&1U))<<15U)|((((w1>>0U)&1U))<<16U)|((((w1>>1U)&1U))<<17U)|((((w1>>2U)&1U))<<18U)|((((w1>>3U)&1U))<<19U)|((((w1>>4U)&1U))<<20U)|((((w1>>5U)&1U))<<21U)|((((w1>>6U)&1U))<<22U)|((((w1>>7U)&1U))<<23U)|((((w1>>8U)&1U))<<24U)|((((w1>>9U)&1U))<<25U)|((((w1>>10U)&1U))<<26U)|((((w1>>11U)&1U))<<27U)|((((w1>>12U)&1U))<<28U)|((((w1>>13U)&1U))<<29U)|((((w1>>14U)&1U))<<30U)|((((w1>>15U)&1U))<<31U);
uint32_t o2=((((w1>>16U)&1U))<<0U)|((((w1>>17U)&1U))<<1U)|((((w1>>18U)&1U))<<2U)|((((w1>>19U)&1U))<<3U)|((((w1>>20U)&1U))<<4U)|((((w1>>21U)&1U))<<5U)|((((w1>>22U)&1U))<<6U)|((((w1>>23U)&1U))<<7U)|((((w1>>24U)&1U))<<8U)|((((w1>>25U)&1U))<<9U)|((((w1>>26U)&1U))<<10U)|((((w1>>27U)&1U))<<11U)|((((w1>>28U)&1U))<<12U)|((((w1>>29U)&1U))<<13U)|((((w1>>30U)&1U))<<14U)|((((w1>>31U)&1U))<<15U)|((((w2>>0U)&1U))<<16U)|((((w2>>1U)&1U))<<17U)|((((w2>>2U)&1U))<<18U)|((((w2>>3U)&1U))<<19U)|((((w2>>4U)&1U))<<20U)|((((w2>>5U)&1U))<<21U)|((((w2>>6U)&1U))<<22U)|((((w2>>7U)&1U))<<23U)|((((w2>>8U)&1U))<<24U)|((((w2>>9U)&1U))<<25U)|((((w2>>10U)&1U))<<26U)|((((w2>>11U)&1U))<<27U)|((((w2>>12U)&1U))<<28U)|((((w2>>13U)&1U))<<29U)|((((w2>>14U)&1U))<<30U)|((((w2>>15U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==4U){
uint32_t o0=0U;
uint32_t o1=((((w1>>16U)&1U))<<0U)|((((w1>>17U)&1U))<<1U)|((((w1>>18U)&1U))<<2U)|((((w1>>19U)&1U))<<3U)|((((w1>>20U)&1U))<<4U)|((((w1>>21U)&1U))<<5U)|((((w1>>22U)&1U))<<6U)|((((w1>>23U)&1U))<<7U)|((((w1>>24U)&1U))<<8U)|((((w1>>25U)&1U))<<9U)|((((w1>>26U)&1U))<<10U)|((((w1>>27U)&1U))<<11U)|((((w1>>28U)&1U))<<12U)|((((w1>>29U)&1U))<<13U)|((((w1>>30U)&1U))<<14U)|((((w1>>31U)&1U))<<15U)|((((w2>>0U)&1U))<<16U)|((((w2>>1U)&1U))<<17U)|((((w2>>2U)&1U))<<18U)|((((w2>>3U)&1U))<<19U)|((((w2>>4U)&1U))<<20U)|((((w2>>5U)&1U))<<21U)|((((w2>>6U)&1U))<<22U)|((((w2>>7U)&1U))<<23U)|((((w2>>8U)&1U))<<24U)|((((w2>>9U)&1U))<<25U)|((((w2>>10U)&1U))<<26U)|((((w2>>11U)&1U))<<27U)|((((w2>>12U)&1U))<<28U)|((((w2>>13U)&1U))<<29U)|((((w2>>14U)&1U))<<30U)|((((w2>>15U)&1U))<<31U);
uint32_t o2=((((w2>>16U)&1U))<<0U)|((((w2>>17U)&1U))<<1U)|((((w2>>18U)&1U))<<2U)|((((w2>>19U)&1U))<<3U)|((((w2>>20U)&1U))<<4U)|((((w2>>21U)&1U))<<5U)|((((w2>>22U)&1U))<<6U)|((((w2>>23U)&1U))<<7U)|((((w2>>24U)&1U))<<8U)|((((w2>>25U)&1U))<<9U)|((((w2>>26U)&1U))<<10U)|((((w2>>27U)&1U))<<11U)|((((w2>>28U)&1U))<<12U)|((((w2>>29U)&1U))<<13U)|((((w2>>30U)&1U))<<14U)|((((w2>>31U)&1U))<<15U)|((((w2>>16U)&1U))<<16U)|((((w2>>17U)&1U))<<17U)|((((w2>>18U)&1U))<<18U)|((((w2>>19U)&1U))<<19U)|((((w2>>20U)&1U))<<20U)|((((w2>>21U)&1U))<<21U)|((((w2>>22U)&1U))<<22U)|((((w2>>23U)&1U))<<23U)|((((w2>>24U)&1U))<<24U)|((((w2>>25U)&1U))<<25U)|((((w2>>26U)&1U))<<26U)|((((w2>>27U)&1U))<<27U)|((((w2>>28U)&1U))<<28U)|((((w2>>29U)&1U))<<29U)|((((w2>>30U)&1U))<<30U)|((((w2>>31U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==5U){
uint32_t o0=0U;
uint32_t o1=w1;
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==6U){
uint32_t o0=((1U)<<2U);
uint32_t o1=w1;
uint32_t o2=((((w1>>24U)&1U))<<0U)|((((w1>>25U)&1U))<<1U)|((((w1>>26U)&1U))<<2U)|((((w1>>27U)&1U))<<3U)|((((w1>>28U)&1U))<<4U)|((((w1>>29U)&1U))<<5U)|((((w1>>30U)&1U))<<6U)|((((w1>>31U)&1U))<<7U)|((((w2>>8U)&1U))<<8U)|((((w2>>9U)&1U))<<9U)|((((w2>>10U)&1U))<<10U)|((((w2>>11U)&1U))<<11U)|((((w2>>12U)&1U))<<12U)|((((w2>>13U)&1U))<<13U)|((((w2>>14U)&1U))<<14U)|((((w2>>15U)&1U))<<15U)|((((w2>>16U)&1U))<<16U)|((((w2>>17U)&1U))<<17U)|((((w2>>18U)&1U))<<18U)|((((w2>>19U)&1U))<<19U)|((((w2>>20U)&1U))<<20U)|((((w2>>21U)&1U))<<21U)|((((w2>>22U)&1U))<<22U)|((((w2>>23U)&1U))<<23U)|((((w2>>24U)&1U))<<24U)|((((w2>>25U)&1U))<<25U)|((((w2>>26U)&1U))<<26U)|((((w2>>27U)&1U))<<27U)|((((w2>>28U)&1U))<<28U)|((((w2>>29U)&1U))<<29U)|((((w2>>30U)&1U))<<30U)|((((w2>>31U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==7U){
uint32_t o0=((1U)<<1U);
uint32_t o1=((((w1>>0U)&1U))<<0U)|((((w1>>1U)&1U))<<1U)|((((w1>>2U)&1U))<<2U)|((((w1>>3U)&1U))<<3U)|((((w1>>4U)&1U))<<4U)|((((w1>>5U)&1U))<<5U)|((((w1>>6U)&1U))<<6U)|((((w1>>7U)&1U))<<7U)|((((w1>>8U)&1U))<<8U)|((((w1>>9U)&1U))<<9U)|((((w1>>10U)&1U))<<10U)|((((w1>>11U)&1U))<<11U)|((((w1>>12U)&1U))<<12U)|((((w1>>13U)&1U))<<13U)|((((w1>>14U)&1U))<<14U)|((((w1>>15U)&1U))<<15U)|((((w1>>8U)&1U))<<16U)|((((w1>>9U)&1U))<<17U)|((((w1>>10U)&1U))<<18U)|((((w1>>11U)&1U))<<19U)|((((w1>>12U)&1U))<<20U)|((((w1>>13U)&1U))<<21U)|((((w1>>14U)&1U))<<22U)|((((w1>>15U)&1U))<<23U)|((((w1>>16U)&1U))<<24U)|((((w1>>17U)&1U))<<25U)|((((w1>>18U)&1U))<<26U)|((((w1>>19U)&1U))<<27U)|((((w1>>20U)&1U))<<28U)|((((w1>>21U)&1U))<<29U)|((((w1>>22U)&1U))<<30U)|((((w1>>23U)&1U))<<31U);
uint32_t o2=((((w1>>24U)&1U))<<0U)|((((w1>>25U)&1U))<<1U)|((((w1>>26U)&1U))<<2U)|((((w1>>27U)&1U))<<3U)|((((w1>>28U)&1U))<<4U)|((((w1>>29U)&1U))<<5U)|((((w1>>30U)&1U))<<6U)|((((w1>>31U)&1U))<<7U)|((((w2>>8U)&1U))<<8U)|((((w2>>9U)&1U))<<9U)|((((w2>>10U)&1U))<<10U)|((((w2>>11U)&1U))<<11U)|((((w2>>12U)&1U))<<12U)|((((w2>>13U)&1U))<<13U)|((((w2>>14U)&1U))<<14U)|((((w2>>15U)&1U))<<15U)|((((w2>>16U)&1U))<<16U)|((((w2>>17U)&1U))<<17U)|((((w2>>18U)&1U))<<18U)|((((w2>>19U)&1U))<<19U)|((((w2>>20U)&1U))<<20U)|((((w2>>21U)&1U))<<21U)|((((w2>>22U)&1U))<<22U)|((((w2>>23U)&1U))<<23U)|((((w2>>24U)&1U))<<24U)|((((w2>>25U)&1U))<<25U)|((((w2>>26U)&1U))<<26U)|((((w2>>27U)&1U))<<27U)|((((w2>>28U)&1U))<<28U)|((((w2>>29U)&1U))<<29U)|((((w2>>30U)&1U))<<30U)|((((w2>>31U)&1U))<<31U);
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
if(cfg==8U){
uint32_t o0=((1U)<<0U);
uint32_t o1=((((w1>>0U)&1U))<<0U)|((((w1>>1U)&1U))<<1U)|((((w1>>2U)&1U))<<2U)|((((w1>>3U)&1U))<<3U)|((((w1>>4U)&1U))<<4U)|((((w1>>5U)&1U))<<5U)|((((w1>>6U)&1U))<<6U)|((((w1>>7U)&1U))<<7U)|((((w1>>16U)&1U))<<8U)|((((w1>>17U)&1U))<<9U)|((((w1>>18U)&1U))<<10U)|((((w1>>19U)&1U))<<11U)|((((w1>>20U)&1U))<<12U)|((((w1>>21U)&1U))<<13U)|((((w1>>22U)&1U))<<14U)|((((w1>>23U)&1U))<<15U)|((((w1>>24U)&1U))<<16U)|((((w1>>25U)&1U))<<17U)|((((w1>>26U)&1U))<<18U)|((((w1>>27U)&1U))<<19U)|((((w1>>28U)&1U))<<20U)|((((w1>>29U)&1U))<<21U)|((((w1>>30U)&1U))<<22U)|((((w1>>31U)&1U))<<23U)|((((w2>>0U)&1U))<<24U)|((((w2>>1U)&1U))<<25U)|((((w2>>2U)&1U))<<26U)|((((w2>>3U)&1U))<<27U)|((((w2>>4U)&1U))<<28U)|((((w2>>5U)&1U))<<29U)|((((w2>>6U)&1U))<<30U)|((((w2>>7U)&1U))<<31U);
uint32_t o2=w2;
b[0]=(unsigned char)(o1>>0U);
b[1]=(unsigned char)(o1>>8U);
b[2]=(unsigned char)(o1>>16U);
b[3]=(unsigned char)(o1>>24U);
b[4]=(unsigned char)(o2>>0U);
b[5]=(unsigned char)(o2>>8U);
b[6]=(unsigned char)(o2>>16U);
b[7]=(unsigned char)(o2>>24U);
return o0;}
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
