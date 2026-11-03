#include <stdint.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8&&sizeof(uint32_t)==4,"ABI");
static unsigned af_parity(uint32_t v){
v^=v>>16;v^=v>>8;v^=v>>4;return (0x6996U>>(v&15U))&1U;}

static uint32_t rf_left(uint32_t x,unsigned cfg,unsigned char *b){
uint32_t w0=x,w1=0,w2=0;
for(unsigned i=0;i<4;i++){w1|=(uint32_t)b[i]<<(8U*i);w2|=(uint32_t)b[i+4]<<(8U*i);}

if(cfg==0U){
uint32_t o0=w0;
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
uint32_t o0=((af_parity(w0&0x00000104U)^af_parity(w1&0x00000004U)^1U)<<0U)|((af_parity(w0&0x00000209U)^af_parity(w1&0x00000009U))<<1U)|((af_parity(w0&0x00000413U)^af_parity(w1&0x00000013U)^1U)<<2U)|((af_parity(w0&0x00000826U)^af_parity(w1&0x00000026U)^1U)<<3U)|((af_parity(w0&0x0000104dU)^af_parity(w1&0x0000004dU))<<4U)|((af_parity(w0&0x0000209aU)^af_parity(w1&0x0000009aU))<<5U)|((af_parity(w0&0x00004030U)^af_parity(w1&0x00000030U))<<6U)|((af_parity(w0&0x00008061U)^af_parity(w1&0x00000061U)^1U)<<7U)|((af_parity(w0&0x000100c2U)^af_parity(w1&0x000000c2U)^1U)<<8U)|((af_parity(w0&0x00020080U)^af_parity(w1&0x00000080U)^1U)<<9U)|((af_parity(w0&0x00040004U)^af_parity(w1&0x00000004U)^1U)<<10U)|((af_parity(w0&0x00080008U)^af_parity(w1&0x00000008U)^1U)<<11U)|((af_parity(w0&0x00100011U)^af_parity(w1&0x00000011U))<<12U)|((af_parity(w0&0x00200023U)^af_parity(w1&0x00000023U)^1U)<<13U)|((af_parity(w0&0x00400046U)^af_parity(w1&0x00000046U)^1U)<<14U)|((af_parity(w0&0x0080008cU)^af_parity(w1&0x0000008cU)^1U)<<15U)|((af_parity(w0&0x0100001dU)^af_parity(w1&0x0000001dU))<<16U)|((af_parity(w0&0x0200003bU)^af_parity(w1&0x0000003bU)^1U)<<17U)|((af_parity(w0&0x04000077U)^af_parity(w1&0x00000077U))<<18U)|((af_parity(w0&0x080000eeU)^af_parity(w1&0x000000eeU))<<19U)|((af_parity(w0&0x100000d8U)^af_parity(w1&0x000000d8U))<<20U)|((af_parity(w0&0x200000b4U)^af_parity(w1&0x000000b4U))<<21U)|((af_parity(w0&0x4000006cU)^af_parity(w1&0x0000006cU))<<22U)|((af_parity(w0&0x800000d8U)^af_parity(w1&0x000000d8U))<<23U)|((af_parity(w0&0x000000b5U)^af_parity(w1&0x000000b5U))<<24U)|((af_parity(w0&0x0000006fU)^af_parity(w1&0x0000006fU)^1U)<<25U)|((af_parity(w0&0x000000dfU)^af_parity(w1&0x000000dfU))<<26U)|((af_parity(w0&0x000000baU)^af_parity(w1&0x000000baU))<<27U)|((af_parity(w0&0x00000071U)^af_parity(w1&0x00000071U)^1U)<<28U)|((af_parity(w0&0x000000e3U)^af_parity(w1&0x000000e3U))<<29U)|((af_parity(w0&0x000000c3U)^af_parity(w1&0x000000c3U)^1U)<<30U)|((af_parity(w0&0x00000082U)^af_parity(w1&0x00000082U)^1U)<<31U);
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
if(cfg==2U){
uint32_t o0=((af_parity(w0&0x000104d1U)^af_parity(w1&0x000004d1U)^1U)<<0U)|((af_parity(w0&0x000209a2U)^af_parity(w1&0x000009a2U)^1U)<<1U)|((af_parity(w0&0x00041344U)^af_parity(w1&0x00001344U)^1U)<<2U)|((af_parity(w0&0x00082688U)^af_parity(w1&0x00002688U)^1U)<<3U)|((af_parity(w0&0x00104d10U)^af_parity(w1&0x00004d10U)^1U)<<4U)|((af_parity(w0&0x00209a20U)^af_parity(w1&0x00009a20U)^1U)<<5U)|((af_parity(w0&0x00403091U)^af_parity(w1&0x00003091U)^1U)<<6U)|((af_parity(w0&0x00806122U)^af_parity(w1&0x00006122U)^1U)<<7U)|((af_parity(w0&0x0100c245U)^af_parity(w1&0x0000c245U))<<8U)|((af_parity(w0&0x0200805aU)^af_parity(w1&0x0000805aU)^1U)<<9U)|((af_parity(w0&0x04000464U)^af_parity(w1&0x00000464U))<<10U)|((af_parity(w0&0x080008c8U)^af_parity(w1&0x000008c8U))<<11U)|((af_parity(w0&0x10001191U)^af_parity(w1&0x00001191U)^1U)<<12U)|((af_parity(w0&0x20002323U)^af_parity(w1&0x00002323U))<<13U)|((af_parity(w0&0x40004646U)^af_parity(w1&0x00004646U))<<14U)|((af_parity(w0&0x80008c8cU)^af_parity(w1&0x00008c8cU))<<15U)|((af_parity(w0&0x00001dc9U)^af_parity(w1&0x00001dc9U)^1U)<<16U)|((af_parity(w0&0x00003b93U)^af_parity(w1&0x00003b93U))<<17U)|((af_parity(w0&0x00007726U)^af_parity(w1&0x00007726U))<<18U)|((af_parity(w0&0x0000ee4dU)^af_parity(w1&0x0000ee4dU)^1U)<<19U)|((af_parity(w0&0x0000d84bU)^af_parity(w1&0x0000d84bU)^1U)<<20U)|((af_parity(w0&0x0000b446U)^af_parity(w1&0x0000b446U))<<21U)|((af_parity(w0&0x00006c5cU)^af_parity(w1&0x00006c5cU)^1U)<<22U)|((af_parity(w0&0x0000d8b8U)^af_parity(w1&0x0000d8b8U)^1U)<<23U)|((af_parity(w0&0x0000b5a1U)^af_parity(w1&0x0000b5a1U)^1U)<<24U)|((af_parity(w0&0x00006f92U)^af_parity(w1&0x00006f92U))<<25U)|((af_parity(w0&0x0000df24U)^af_parity(w1&0x0000df24U))<<26U)|((af_parity(w0&0x0000ba99U)^af_parity(w1&0x0000ba99U))<<27U)|((af_parity(w0&0x000071e3U)^af_parity(w1&0x000071e3U))<<28U)|((af_parity(w0&0x0000e3c6U)^af_parity(w1&0x0000e3c6U))<<29U)|((af_parity(w0&0x0000c35cU)^af_parity(w1&0x0000c35cU)^1U)<<30U)|((af_parity(w0&0x00008268U)^af_parity(w1&0x00008268U))<<31U);
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
if(cfg==3U){
uint32_t o0=((af_parity(w0&0x0104d101U)^af_parity(w1&0x0004d101U))<<0U)|((af_parity(w0&0x0209a203U)^af_parity(w1&0x0009a203U)^1U)<<1U)|((af_parity(w0&0x04134407U)^af_parity(w1&0x00134407U))<<2U)|((af_parity(w0&0x0826880eU)^af_parity(w1&0x0026880eU))<<3U)|((af_parity(w0&0x104d101dU)^af_parity(w1&0x004d101dU)^1U)<<4U)|((af_parity(w0&0x209a203bU)^af_parity(w1&0x009a203bU))<<5U)|((af_parity(w0&0x40309176U)^af_parity(w1&0x00309176U))<<6U)|((af_parity(w0&0x806122ecU)^af_parity(w1&0x006122ecU))<<7U)|((af_parity(w0&0x00c245d8U)^af_parity(w1&0x00c245d8U)^1U)<<8U)|((af_parity(w0&0x00805ab1U)^af_parity(w1&0x00805ab1U))<<9U)|((af_parity(w0&0x00046462U)^af_parity(w1&0x00046462U))<<10U)|((af_parity(w0&0x0008c8c5U)^af_parity(w1&0x0008c8c5U)^1U)<<11U)|((af_parity(w0&0x0011918aU)^af_parity(w1&0x0011918aU)^1U)<<12U)|((af_parity(w0&0x00232315U)^af_parity(w1&0x00232315U))<<13U)|((af_parity(w0&0x0046462bU)^af_parity(w1&0x0046462bU)^1U)<<14U)|((af_parity(w0&0x008c8c56U)^af_parity(w1&0x008c8c56U)^1U)<<15U)|((af_parity(w0&0x001dc9acU)^af_parity(w1&0x001dc9acU)^1U)<<16U)|((af_parity(w0&0x003b9359U)^af_parity(w1&0x003b9359U))<<17U)|((af_parity(w0&0x007726b2U)^af_parity(w1&0x007726b2U))<<18U)|((af_parity(w0&0x00ee4d64U)^af_parity(w1&0x00ee4d64U))<<19U)|((af_parity(w0&0x00d84bc8U)^af_parity(w1&0x00d84bc8U))<<20U)|((af_parity(w0&0x00b44690U)^af_parity(w1&0x00b44690U))<<21U)|((af_parity(w0&0x006c5c21U)^af_parity(w1&0x006c5c21U)^1U)<<22U)|((af_parity(w0&0x00d8b843U)^af_parity(w1&0x00d8b843U))<<23U)|((af_parity(w0&0x00b5a187U)^af_parity(w1&0x00b5a187U)^1U)<<24U)|((af_parity(w0&0x006f920eU)^af_parity(w1&0x006f920eU)^1U)<<25U)|((af_parity(w0&0x00df241cU)^af_parity(w1&0x00df241cU)^1U)<<26U)|((af_parity(w0&0x00ba9938U)^af_parity(w1&0x00ba9938U)^1U)<<27U)|((af_parity(w0&0x0071e370U)^af_parity(w1&0x0071e370U)^1U)<<28U)|((af_parity(w0&0x00e3c6e0U)^af_parity(w1&0x00e3c6e0U)^1U)<<29U)|((af_parity(w0&0x00c35cc0U)^af_parity(w1&0x00c35cc0U)^1U)<<30U)|((af_parity(w0&0x00826880U)^af_parity(w1&0x00826880U)^1U)<<31U);
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
if(cfg==4U){
uint32_t o0=((af_parity(w0&0x04d101dfU)^af_parity(w1&0x04d101dfU))<<0U)|((af_parity(w0&0x09a203beU)^af_parity(w1&0x09a203beU))<<1U)|((af_parity(w0&0x1344077dU)^af_parity(w1&0x1344077dU)^1U)<<2U)|((af_parity(w0&0x26880efaU)^af_parity(w1&0x26880efaU)^1U)<<3U)|((af_parity(w0&0x4d101df4U)^af_parity(w1&0x4d101df4U)^1U)<<4U)|((af_parity(w0&0x9a203be9U)^af_parity(w1&0x9a203be9U))<<5U)|((af_parity(w0&0x3091760dU)^af_parity(w1&0x3091760dU))<<6U)|((af_parity(w0&0x6122ec1aU)^af_parity(w1&0x6122ec1aU))<<7U)|((af_parity(w0&0xc245d835U)^af_parity(w1&0xc245d835U)^1U)<<8U)|((af_parity(w0&0x805ab1b5U)^af_parity(w1&0x805ab1b5U)^1U)<<9U)|((af_parity(w0&0x046462b5U)^af_parity(w1&0x046462b5U)^1U)<<10U)|((af_parity(w0&0x08c8c56aU)^af_parity(w1&0x08c8c56aU)^1U)<<11U)|((af_parity(w0&0x11918ad4U)^af_parity(w1&0x11918ad4U)^1U)<<12U)|((af_parity(w0&0x232315a9U)^af_parity(w1&0x232315a9U))<<13U)|((af_parity(w0&0x46462b53U)^af_parity(w1&0x46462b53U)^1U)<<14U)|((af_parity(w0&0x8c8c56a6U)^af_parity(w1&0x8c8c56a6U)^1U)<<15U)|((af_parity(w0&0x1dc9ac92U)^af_parity(w1&0x1dc9ac92U))<<16U)|((af_parity(w0&0x3b935924U)^af_parity(w1&0x3b935924U))<<17U)|((af_parity(w0&0x7726b249U)^af_parity(w1&0x7726b249U)^1U)<<18U)|((af_parity(w0&0xee4d6493U)^af_parity(w1&0xee4d6493U))<<19U)|((af_parity(w0&0xd84bc8f9U)^af_parity(w1&0xd84bc8f9U))<<20U)|((af_parity(w0&0xb446902dU)^af_parity(w1&0xb446902dU))<<21U)|((af_parity(w0&0x6c5c2184U)^af_parity(w1&0x6c5c2184U)^1U)<<22U)|((af_parity(w0&0xd8b84309U)^af_parity(w1&0xd8b84309U))<<23U)|((af_parity(w0&0xb5a187ccU)^af_parity(w1&0xb5a187ccU)^1U)<<24U)|((af_parity(w0&0x6f920e46U)^af_parity(w1&0x6f920e46U))<<25U)|((af_parity(w0&0xdf241c8cU)^af_parity(w1&0xdf241c8cU))<<26U)|((af_parity(w0&0xba9938c7U)^af_parity(w1&0xba9938c7U))<<27U)|((af_parity(w0&0x71e37051U)^af_parity(w1&0x71e37051U))<<28U)|((af_parity(w0&0xe3c6e0a3U)^af_parity(w1&0xe3c6e0a3U)^1U)<<29U)|((af_parity(w0&0xc35cc098U)^af_parity(w1&0xc35cc098U))<<30U)|((af_parity(w0&0x826880efU)^af_parity(w1&0x826880efU))<<31U);
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
if(cfg==5U){
uint32_t o0=((af_parity(w0&0xd101df48U)^af_parity(w1&0xd101df48U)^af_parity(w2&0x00000004U)^1U)<<0U)|((af_parity(w0&0xa203be90U)^af_parity(w1&0xa203be90U)^af_parity(w2&0x00000009U))<<1U)|((af_parity(w0&0x44077d20U)^af_parity(w1&0x44077d20U)^af_parity(w2&0x00000013U)^1U)<<2U)|((af_parity(w0&0x880efa40U)^af_parity(w1&0x880efa40U)^af_parity(w2&0x00000026U)^1U)<<3U)|((af_parity(w0&0x101df481U)^af_parity(w1&0x101df481U)^af_parity(w2&0x0000004dU)^1U)<<4U)|((af_parity(w0&0x203be903U)^af_parity(w1&0x203be903U)^af_parity(w2&0x0000009aU))<<5U)|((af_parity(w0&0x91760d4eU)^af_parity(w1&0x91760d4eU)^af_parity(w2&0x00000030U))<<6U)|((af_parity(w0&0x22ec1a9dU)^af_parity(w1&0x22ec1a9dU)^af_parity(w2&0x00000061U))<<7U)|((af_parity(w0&0x45d8353bU)^af_parity(w1&0x45d8353bU)^af_parity(w2&0x000000c2U)^1U)<<8U)|((af_parity(w0&0x5ab1b53eU)^af_parity(w1&0x5ab1b53eU)^af_parity(w2&0x00000080U)^1U)<<9U)|((af_parity(w0&0x6462b534U)^af_parity(w1&0x6462b534U)^af_parity(w2&0x00000004U)^1U)<<10U)|((af_parity(w0&0xc8c56a69U)^af_parity(w1&0xc8c56a69U)^af_parity(w2&0x00000008U))<<11U)|((af_parity(w0&0x918ad4d2U)^af_parity(w1&0x918ad4d2U)^af_parity(w2&0x00000011U)^1U)<<12U)|((af_parity(w0&0x2315a9a5U)^af_parity(w1&0x2315a9a5U)^af_parity(w2&0x00000023U)^1U)<<13U)|((af_parity(w0&0x462b534aU)^af_parity(w1&0x462b534aU)^af_parity(w2&0x00000046U)^1U)<<14U)|((af_parity(w0&0x8c56a694U)^af_parity(w1&0x8c56a694U)^af_parity(w2&0x0000008cU)^1U)<<15U)|((af_parity(w0&0xc9ac9260U)^af_parity(w1&0xc9ac9260U)^af_parity(w2&0x0000001dU))<<16U)|((af_parity(w0&0x935924c0U)^af_parity(w1&0x935924c0U)^af_parity(w2&0x0000003bU)^1U)<<17U)|((af_parity(w0&0x26b24980U)^af_parity(w1&0x26b24980U)^af_parity(w2&0x00000077U))<<18U)|((af_parity(w0&0x4d649300U)^af_parity(w1&0x4d649300U)^af_parity(w2&0x000000eeU))<<19U)|((af_parity(w0&0x4bc8f948U)^af_parity(w1&0x4bc8f948U)^af_parity(w2&0x000000d8U))<<20U)|((af_parity(w0&0x46902dd9U)^af_parity(w1&0x46902dd9U)^af_parity(w2&0x000000b4U)^1U)<<21U)|((af_parity(w0&0x5c2184fbU)^af_parity(w1&0x5c2184fbU)^af_parity(w2&0x0000006cU))<<22U)|((af_parity(w0&0xb84309f6U)^af_parity(w1&0xb84309f6U)^af_parity(w2&0x000000d8U))<<23U)|((af_parity(w0&0xa187cca5U)^af_parity(w1&0xa187cca5U)^af_parity(w2&0x000000b5U))<<24U)|((af_parity(w0&0x920e4602U)^af_parity(w1&0x920e4602U)^af_parity(w2&0x0000006fU)^1U)<<25U)|((af_parity(w0&0x241c8c05U)^af_parity(w1&0x241c8c05U)^af_parity(w2&0x000000dfU)^1U)<<26U)|((af_parity(w0&0x9938c743U)^af_parity(w1&0x9938c743U)^af_parity(w2&0x000000baU))<<27U)|((af_parity(w0&0xe37051cfU)^af_parity(w1&0xe37051cfU)^af_parity(w2&0x00000071U))<<28U)|((af_parity(w0&0xc6e0a39fU)^af_parity(w1&0xc6e0a39fU)^af_parity(w2&0x000000e3U))<<29U)|((af_parity(w0&0x5cc09876U)^af_parity(w1&0x5cc09876U)^af_parity(w2&0x000000c3U)^1U)<<30U)|((af_parity(w0&0x6880efa4U)^af_parity(w1&0x6880efa4U)^af_parity(w2&0x00000082U)^1U)<<31U);
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
uint32_t o0=((af_parity(w0&0x01df481bU)^af_parity(w1&0x01df481bU)^af_parity(w2&0x000004d1U)^1U)<<0U)|((af_parity(w0&0x03be9036U)^af_parity(w1&0x03be9036U)^af_parity(w2&0x000009a2U)^1U)<<1U)|((af_parity(w0&0x077d206dU)^af_parity(w1&0x077d206dU)^af_parity(w2&0x00001344U))<<2U)|((af_parity(w0&0x0efa40daU)^af_parity(w1&0x0efa40daU)^af_parity(w2&0x00002688U))<<3U)|((af_parity(w0&0x1df481b4U)^af_parity(w1&0x1df481b4U)^af_parity(w2&0x00004d10U))<<4U)|((af_parity(w0&0x3be90369U)^af_parity(w1&0x3be90369U)^af_parity(w2&0x00009a20U)^1U)<<5U)|((af_parity(w0&0x760d4ec8U)^af_parity(w1&0x760d4ec8U)^af_parity(w2&0x00003091U))<<6U)|((af_parity(w0&0xec1a9d91U)^af_parity(w1&0xec1a9d91U)^af_parity(w2&0x00006122U)^1U)<<7U)|((af_parity(w0&0xd8353b23U)^af_parity(w1&0xd8353b23U)^af_parity(w2&0x0000c245U)^1U)<<8U)|((af_parity(w0&0xb1b53e5dU)^af_parity(w1&0xb1b53e5dU)^af_parity(w2&0x0000805aU))<<9U)|((af_parity(w0&0x62b534a0U)^af_parity(w1&0x62b534a0U)^af_parity(w2&0x00000464U))<<10U)|((af_parity(w0&0xc56a6940U)^af_parity(w1&0xc56a6940U)^af_parity(w2&0x000008c8U))<<11U)|((af_parity(w0&0x8ad4d281U)^af_parity(w1&0x8ad4d281U)^af_parity(w2&0x00001191U))<<12U)|((af_parity(w0&0x15a9a502U)^af_parity(w1&0x15a9a502U)^af_parity(w2&0x00002323U)^1U)<<13U)|((af_parity(w0&0x2b534a05U)^af_parity(w1&0x2b534a05U)^af_parity(w2&0x00004646U))<<14U)|((af_parity(w0&0x56a6940bU)^af_parity(w1&0x56a6940bU)^af_parity(w2&0x00008c8cU)^1U)<<15U)|((af_parity(w0&0xac92600cU)^af_parity(w1&0xac92600cU)^af_parity(w2&0x00001dc9U))<<16U)|((af_parity(w0&0x5924c018U)^af_parity(w1&0x5924c018U)^af_parity(w2&0x00003b93U)^1U)<<17U)|((af_parity(w0&0xb2498031U)^af_parity(w1&0xb2498031U)^af_parity(w2&0x00007726U))<<18U)|((af_parity(w0&0x64930063U)^af_parity(w1&0x64930063U)^af_parity(w2&0x0000ee4dU))<<19U)|((af_parity(w0&0xc8f948ddU)^af_parity(w1&0xc8f948ddU)^af_parity(w2&0x0000d84bU))<<20U)|((af_parity(w0&0x902dd9a0U)^af_parity(w1&0x902dd9a0U)^af_parity(w2&0x0000b446U))<<21U)|((af_parity(w0&0x2184fb5bU)^af_parity(w1&0x2184fb5bU)^af_parity(w2&0x00006c5cU)^1U)<<22U)|((af_parity(w0&0x4309f6b6U)^af_parity(w1&0x4309f6b6U)^af_parity(w2&0x0000d8b8U)^1U)<<23U)|((af_parity(w0&0x87cca577U)^af_parity(w1&0x87cca577U)^af_parity(w2&0x0000b5a1U)^1U)<<24U)|((af_parity(w0&0x0e4602f5U)^af_parity(w1&0x0e4602f5U)^af_parity(w2&0x00006f92U))<<25U)|((af_parity(w0&0x1c8c05eaU)^af_parity(w1&0x1c8c05eaU)^af_parity(w2&0x0000df24U))<<26U)|((af_parity(w0&0x38c743cfU)^af_parity(w1&0x38c743cfU)^af_parity(w2&0x0000ba99U))<<27U)|((af_parity(w0&0x7051cf84U)^af_parity(w1&0x7051cf84U)^af_parity(w2&0x000071e3U)^1U)<<28U)|((af_parity(w0&0xe0a39f08U)^af_parity(w1&0xe0a39f08U)^af_parity(w2&0x0000e3c6U)^1U)<<29U)|((af_parity(w0&0xc098760bU)^af_parity(w1&0xc098760bU)^af_parity(w2&0x0000c35cU))<<30U)|((af_parity(w0&0x80efa40dU)^af_parity(w1&0x80efa40dU)^af_parity(w2&0x00008268U)^1U)<<31U);
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
if(cfg==7U){
uint32_t o0=((af_parity(w0&0xdf481b4eU)^af_parity(w1&0xdf481b4eU)^af_parity(w2&0x0004d101U))<<0U)|((af_parity(w0&0xbe90369cU)^af_parity(w1&0xbe90369cU)^af_parity(w2&0x0009a203U)^1U)<<1U)|((af_parity(w0&0x7d206d39U)^af_parity(w1&0x7d206d39U)^af_parity(w2&0x00134407U)^1U)<<2U)|((af_parity(w0&0xfa40da72U)^af_parity(w1&0xfa40da72U)^af_parity(w2&0x0026880eU)^1U)<<3U)|((af_parity(w0&0xf481b4e5U)^af_parity(w1&0xf481b4e5U)^af_parity(w2&0x004d101dU)^1U)<<4U)|((af_parity(w0&0xe90369cbU)^af_parity(w1&0xe90369cbU)^af_parity(w2&0x009a203bU)^1U)<<5U)|((af_parity(w0&0x0d4ec8d8U)^af_parity(w1&0x0d4ec8d8U)^af_parity(w2&0x00309176U)^1U)<<6U)|((af_parity(w0&0x1a9d91b1U)^af_parity(w1&0x1a9d91b1U)^af_parity(w2&0x006122ecU))<<7U)|((af_parity(w0&0x353b2363U)^af_parity(w1&0x353b2363U)^af_parity(w2&0x00c245d8U)^1U)<<8U)|((af_parity(w0&0xb53e5d89U)^af_parity(w1&0xb53e5d89U)^af_parity(w2&0x00805ab1U)^1U)<<9U)|((af_parity(w0&0xb534a05cU)^af_parity(w1&0xb534a05cU)^af_parity(w2&0x00046462U)^1U)<<10U)|((af_parity(w0&0x6a6940b9U)^af_parity(w1&0x6a6940b9U)^af_parity(w2&0x0008c8c5U)^1U)<<11U)|((af_parity(w0&0xd4d28172U)^af_parity(w1&0xd4d28172U)^af_parity(w2&0x0011918aU)^1U)<<12U)|((af_parity(w0&0xa9a502e4U)^af_parity(w1&0xa9a502e4U)^af_parity(w2&0x00232315U))<<13U)|((af_parity(w0&0x534a05c8U)^af_parity(w1&0x534a05c8U)^af_parity(w2&0x0046462bU)^1U)<<14U)|((af_parity(w0&0xa6940b90U)^af_parity(w1&0xa6940b90U)^af_parity(w2&0x008c8c56U)^1U)<<15U)|((af_parity(w0&0x92600c6fU)^af_parity(w1&0x92600c6fU)^af_parity(w2&0x001dc9acU))<<16U)|((af_parity(w0&0x24c018dfU)^af_parity(w1&0x24c018dfU)^af_parity(w2&0x003b9359U))<<17U)|((af_parity(w0&0x498031bfU)^af_parity(w1&0x498031bfU)^af_parity(w2&0x007726b2U)^1U)<<18U)|((af_parity(w0&0x9300637eU)^af_parity(w1&0x9300637eU)^af_parity(w2&0x00ee4d64U)^1U)<<19U)|((af_parity(w0&0xf948ddb3U)^af_parity(w1&0xf948ddb3U)^af_parity(w2&0x00d84bc8U))<<20U)|((af_parity(w0&0x2dd9a029U)^af_parity(w1&0x2dd9a029U)^af_parity(w2&0x00b44690U)^1U)<<21U)|((af_parity(w0&0x84fb5b1dU)^af_parity(w1&0x84fb5b1dU)^af_parity(w2&0x006c5c21U)^1U)<<22U)|((af_parity(w0&0x09f6b63aU)^af_parity(w1&0x09f6b63aU)^af_parity(w2&0x00d8b843U))<<23U)|((af_parity(w0&0xcca5773aU)^af_parity(w1&0xcca5773aU)^af_parity(w2&0x00b5a187U)^1U)<<24U)|((af_parity(w0&0x4602f53bU)^af_parity(w1&0x4602f53bU)^af_parity(w2&0x006f920eU))<<25U)|((af_parity(w0&0x8c05ea77U)^af_parity(w1&0x8c05ea77U)^af_parity(w2&0x00df241cU)^1U)<<26U)|((af_parity(w0&0xc743cfa0U)^af_parity(w1&0xc743cfa0U)^af_parity(w2&0x00ba9938U)^1U)<<27U)|((af_parity(w0&0x51cf840eU)^af_parity(w1&0x51cf840eU)^af_parity(w2&0x0071e370U)^1U)<<28U)|((af_parity(w0&0xa39f081dU)^af_parity(w1&0xa39f081dU)^af_parity(w2&0x00e3c6e0U))<<29U)|((af_parity(w0&0x98760b74U)^af_parity(w1&0x98760b74U)^af_parity(w2&0x00c35cc0U))<<30U)|((af_parity(w0&0xefa40da7U)^af_parity(w1&0xefa40da7U)^af_parity(w2&0x00826880U)^1U)<<31U);
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
if(cfg==8U){
uint32_t o0=((af_parity(w0&0x481b4e5aU)^af_parity(w1&0x481b4e5aU)^af_parity(w2&0x04d101dfU)^1U)<<0U)|((af_parity(w0&0x90369cb5U)^af_parity(w1&0x90369cb5U)^af_parity(w2&0x09a203beU))<<1U)|((af_parity(w0&0x206d396bU)^af_parity(w1&0x206d396bU)^af_parity(w2&0x1344077dU))<<2U)|((af_parity(w0&0x40da72d7U)^af_parity(w1&0x40da72d7U)^af_parity(w2&0x26880efaU)^1U)<<3U)|((af_parity(w0&0x81b4e5afU)^af_parity(w1&0x81b4e5afU)^af_parity(w2&0x4d101df4U))<<4U)|((af_parity(w0&0x0369cb5eU)^af_parity(w1&0x0369cb5eU)^af_parity(w2&0x9a203be9U)^1U)<<5U)|((af_parity(w0&0x4ec8d8e6U)^af_parity(w1&0x4ec8d8e6U)^af_parity(w2&0x3091760dU)^1U)<<6U)|((af_parity(w0&0x9d91b1cdU)^af_parity(w1&0x9d91b1cdU)^af_parity(w2&0x6122ec1aU))<<7U)|((af_parity(w0&0x3b23639aU)^af_parity(w1&0x3b23639aU)^af_parity(w2&0xc245d835U)^1U)<<8U)|((af_parity(w0&0x3e5d896eU)^af_parity(w1&0x3e5d896eU)^af_parity(w2&0x805ab1b5U)^1U)<<9U)|((af_parity(w0&0x34a05c86U)^af_parity(w1&0x34a05c86U)^af_parity(w2&0x046462b5U)^1U)<<10U)|((af_parity(w0&0x6940b90cU)^af_parity(w1&0x6940b90cU)^af_parity(w2&0x08c8c56aU)^1U)<<11U)|((af_parity(w0&0xd2817218U)^af_parity(w1&0xd2817218U)^af_parity(w2&0x11918ad4U)^1U)<<12U)|((af_parity(w0&0xa502e430U)^af_parity(w1&0xa502e430U)^af_parity(w2&0x232315a9U))<<13U)|((af_parity(w0&0x4a05c860U)^af_parity(w1&0x4a05c860U)^af_parity(w2&0x46462b53U)^1U)<<14U)|((af_parity(w0&0x940b90c0U)^af_parity(w1&0x940b90c0U)^af_parity(w2&0x8c8c56a6U)^1U)<<15U)|((af_parity(w0&0x600c6fdaU)^af_parity(w1&0x600c6fdaU)^af_parity(w2&0x1dc9ac92U))<<16U)|((af_parity(w0&0xc018dfb5U)^af_parity(w1&0xc018dfb5U)^af_parity(w2&0x3b935924U)^1U)<<17U)|((af_parity(w0&0x8031bf6aU)^af_parity(w1&0x8031bf6aU)^af_parity(w2&0x7726b249U))<<18U)|((af_parity(w0&0x00637ed5U)^af_parity(w1&0x00637ed5U)^af_parity(w2&0xee4d6493U))<<19U)|((af_parity(w0&0x48ddb3f0U)^af_parity(w1&0x48ddb3f0U)^af_parity(w2&0xd84bc8f9U))<<20U)|((af_parity(w0&0xd9a029bbU)^af_parity(w1&0xd9a029bbU)^af_parity(w2&0xb446902dU)^1U)<<21U)|((af_parity(w0&0xfb5b1d2cU)^af_parity(w1&0xfb5b1d2cU)^af_parity(w2&0x6c5c2184U))<<22U)|((af_parity(w0&0xf6b63a59U)^af_parity(w1&0xf6b63a59U)^af_parity(w2&0xd8b84309U))<<23U)|((af_parity(w0&0xa5773ae8U)^af_parity(w1&0xa5773ae8U)^af_parity(w2&0xb5a187ccU)^1U)<<24U)|((af_parity(w0&0x02f53b8aU)^af_parity(w1&0x02f53b8aU)^af_parity(w2&0x6f920e46U))<<25U)|((af_parity(w0&0x05ea7715U)^af_parity(w1&0x05ea7715U)^af_parity(w2&0xdf241c8cU)^1U)<<26U)|((af_parity(w0&0x43cfa071U)^af_parity(w1&0x43cfa071U)^af_parity(w2&0xba9938c7U))<<27U)|((af_parity(w0&0xcf840eb8U)^af_parity(w1&0xcf840eb8U)^af_parity(w2&0x71e37051U))<<28U)|((af_parity(w0&0x9f081d70U)^af_parity(w1&0x9f081d70U)^af_parity(w2&0xe3c6e0a3U)^1U)<<29U)|((af_parity(w0&0x760b74bbU)^af_parity(w1&0x760b74bbU)^af_parity(w2&0xc35cc098U)^1U)<<30U)|((af_parity(w0&0xa40da72dU)^af_parity(w1&0xa40da72dU)^af_parity(w2&0x826880efU))<<31U);
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
return 0U;}
static uint32_t rf_right(uint32_t x,unsigned cfg,unsigned char *b){
uint32_t w0=x,w1=0,w2=0;
for(unsigned i=0;i<4;i++){w1|=(uint32_t)b[i]<<(8U*i);w2|=(uint32_t)b[i+4]<<(8U*i);}

if(cfg==0U){
uint32_t o0=w0;
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
uint32_t o0=((af_parity(w0&0x00000104U)^af_parity(w1&0x00000004U)^1U)<<0U)|((af_parity(w0&0x00000209U)^af_parity(w1&0x00000009U))<<1U)|((af_parity(w0&0x00000413U)^af_parity(w1&0x00000013U)^1U)<<2U)|((af_parity(w0&0x00000826U)^af_parity(w1&0x00000026U)^1U)<<3U)|((af_parity(w0&0x0000104dU)^af_parity(w1&0x0000004dU))<<4U)|((af_parity(w0&0x0000209aU)^af_parity(w1&0x0000009aU))<<5U)|((af_parity(w0&0x00004030U)^af_parity(w1&0x00000030U))<<6U)|((af_parity(w0&0x00008061U)^af_parity(w1&0x00000061U)^1U)<<7U)|((af_parity(w0&0x000100c2U)^af_parity(w1&0x000000c2U)^1U)<<8U)|((af_parity(w0&0x00020080U)^af_parity(w1&0x00000080U)^1U)<<9U)|((af_parity(w0&0x00040004U)^af_parity(w1&0x00000004U)^1U)<<10U)|((af_parity(w0&0x00080008U)^af_parity(w1&0x00000008U)^1U)<<11U)|((af_parity(w0&0x00100011U)^af_parity(w1&0x00000011U))<<12U)|((af_parity(w0&0x00200023U)^af_parity(w1&0x00000023U)^1U)<<13U)|((af_parity(w0&0x00400046U)^af_parity(w1&0x00000046U)^1U)<<14U)|((af_parity(w0&0x0080008cU)^af_parity(w1&0x0000008cU)^1U)<<15U)|((af_parity(w0&0x0100001dU)^af_parity(w1&0x0000001dU))<<16U)|((af_parity(w0&0x0200003bU)^af_parity(w1&0x0000003bU)^1U)<<17U)|((af_parity(w0&0x04000077U)^af_parity(w1&0x00000077U))<<18U)|((af_parity(w0&0x080000eeU)^af_parity(w1&0x000000eeU))<<19U)|((af_parity(w0&0x100000d8U)^af_parity(w1&0x000000d8U))<<20U)|((af_parity(w0&0x200000b4U)^af_parity(w1&0x000000b4U))<<21U)|((af_parity(w0&0x4000006cU)^af_parity(w1&0x0000006cU))<<22U)|((af_parity(w0&0x800000d8U)^af_parity(w1&0x000000d8U))<<23U)|((af_parity(w0&0x000000b5U)^af_parity(w1&0x000000b5U))<<24U)|((af_parity(w0&0x0000006fU)^af_parity(w1&0x0000006fU)^1U)<<25U)|((af_parity(w0&0x000000dfU)^af_parity(w1&0x000000dfU))<<26U)|((af_parity(w0&0x000000baU)^af_parity(w1&0x000000baU))<<27U)|((af_parity(w0&0x00000071U)^af_parity(w1&0x00000071U)^1U)<<28U)|((af_parity(w0&0x000000e3U)^af_parity(w1&0x000000e3U))<<29U)|((af_parity(w0&0x000000c3U)^af_parity(w1&0x000000c3U)^1U)<<30U)|((af_parity(w0&0x00000082U)^af_parity(w1&0x00000082U)^1U)<<31U);
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
if(cfg==2U){
uint32_t o0=((af_parity(w0&0x000104d1U)^af_parity(w1&0x000004d1U)^1U)<<0U)|((af_parity(w0&0x000209a2U)^af_parity(w1&0x000009a2U)^1U)<<1U)|((af_parity(w0&0x00041344U)^af_parity(w1&0x00001344U)^1U)<<2U)|((af_parity(w0&0x00082688U)^af_parity(w1&0x00002688U)^1U)<<3U)|((af_parity(w0&0x00104d10U)^af_parity(w1&0x00004d10U)^1U)<<4U)|((af_parity(w0&0x00209a20U)^af_parity(w1&0x00009a20U)^1U)<<5U)|((af_parity(w0&0x00403091U)^af_parity(w1&0x00003091U)^1U)<<6U)|((af_parity(w0&0x00806122U)^af_parity(w1&0x00006122U)^1U)<<7U)|((af_parity(w0&0x0100c245U)^af_parity(w1&0x0000c245U))<<8U)|((af_parity(w0&0x0200805aU)^af_parity(w1&0x0000805aU)^1U)<<9U)|((af_parity(w0&0x04000464U)^af_parity(w1&0x00000464U))<<10U)|((af_parity(w0&0x080008c8U)^af_parity(w1&0x000008c8U))<<11U)|((af_parity(w0&0x10001191U)^af_parity(w1&0x00001191U)^1U)<<12U)|((af_parity(w0&0x20002323U)^af_parity(w1&0x00002323U))<<13U)|((af_parity(w0&0x40004646U)^af_parity(w1&0x00004646U))<<14U)|((af_parity(w0&0x80008c8cU)^af_parity(w1&0x00008c8cU))<<15U)|((af_parity(w0&0x00001dc9U)^af_parity(w1&0x00001dc9U)^1U)<<16U)|((af_parity(w0&0x00003b93U)^af_parity(w1&0x00003b93U))<<17U)|((af_parity(w0&0x00007726U)^af_parity(w1&0x00007726U))<<18U)|((af_parity(w0&0x0000ee4dU)^af_parity(w1&0x0000ee4dU)^1U)<<19U)|((af_parity(w0&0x0000d84bU)^af_parity(w1&0x0000d84bU)^1U)<<20U)|((af_parity(w0&0x0000b446U)^af_parity(w1&0x0000b446U))<<21U)|((af_parity(w0&0x00006c5cU)^af_parity(w1&0x00006c5cU)^1U)<<22U)|((af_parity(w0&0x0000d8b8U)^af_parity(w1&0x0000d8b8U)^1U)<<23U)|((af_parity(w0&0x0000b5a1U)^af_parity(w1&0x0000b5a1U)^1U)<<24U)|((af_parity(w0&0x00006f92U)^af_parity(w1&0x00006f92U))<<25U)|((af_parity(w0&0x0000df24U)^af_parity(w1&0x0000df24U))<<26U)|((af_parity(w0&0x0000ba99U)^af_parity(w1&0x0000ba99U))<<27U)|((af_parity(w0&0x000071e3U)^af_parity(w1&0x000071e3U))<<28U)|((af_parity(w0&0x0000e3c6U)^af_parity(w1&0x0000e3c6U))<<29U)|((af_parity(w0&0x0000c35cU)^af_parity(w1&0x0000c35cU)^1U)<<30U)|((af_parity(w0&0x00008268U)^af_parity(w1&0x00008268U))<<31U);
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
if(cfg==3U){
uint32_t o0=((af_parity(w0&0x0104d101U)^af_parity(w1&0x0004d101U))<<0U)|((af_parity(w0&0x0209a203U)^af_parity(w1&0x0009a203U)^1U)<<1U)|((af_parity(w0&0x04134407U)^af_parity(w1&0x00134407U))<<2U)|((af_parity(w0&0x0826880eU)^af_parity(w1&0x0026880eU))<<3U)|((af_parity(w0&0x104d101dU)^af_parity(w1&0x004d101dU)^1U)<<4U)|((af_parity(w0&0x209a203bU)^af_parity(w1&0x009a203bU))<<5U)|((af_parity(w0&0x40309176U)^af_parity(w1&0x00309176U))<<6U)|((af_parity(w0&0x806122ecU)^af_parity(w1&0x006122ecU))<<7U)|((af_parity(w0&0x00c245d8U)^af_parity(w1&0x00c245d8U)^1U)<<8U)|((af_parity(w0&0x00805ab1U)^af_parity(w1&0x00805ab1U))<<9U)|((af_parity(w0&0x00046462U)^af_parity(w1&0x00046462U))<<10U)|((af_parity(w0&0x0008c8c5U)^af_parity(w1&0x0008c8c5U)^1U)<<11U)|((af_parity(w0&0x0011918aU)^af_parity(w1&0x0011918aU)^1U)<<12U)|((af_parity(w0&0x00232315U)^af_parity(w1&0x00232315U))<<13U)|((af_parity(w0&0x0046462bU)^af_parity(w1&0x0046462bU)^1U)<<14U)|((af_parity(w0&0x008c8c56U)^af_parity(w1&0x008c8c56U)^1U)<<15U)|((af_parity(w0&0x001dc9acU)^af_parity(w1&0x001dc9acU)^1U)<<16U)|((af_parity(w0&0x003b9359U)^af_parity(w1&0x003b9359U))<<17U)|((af_parity(w0&0x007726b2U)^af_parity(w1&0x007726b2U))<<18U)|((af_parity(w0&0x00ee4d64U)^af_parity(w1&0x00ee4d64U))<<19U)|((af_parity(w0&0x00d84bc8U)^af_parity(w1&0x00d84bc8U))<<20U)|((af_parity(w0&0x00b44690U)^af_parity(w1&0x00b44690U))<<21U)|((af_parity(w0&0x006c5c21U)^af_parity(w1&0x006c5c21U)^1U)<<22U)|((af_parity(w0&0x00d8b843U)^af_parity(w1&0x00d8b843U))<<23U)|((af_parity(w0&0x00b5a187U)^af_parity(w1&0x00b5a187U)^1U)<<24U)|((af_parity(w0&0x006f920eU)^af_parity(w1&0x006f920eU)^1U)<<25U)|((af_parity(w0&0x00df241cU)^af_parity(w1&0x00df241cU)^1U)<<26U)|((af_parity(w0&0x00ba9938U)^af_parity(w1&0x00ba9938U)^1U)<<27U)|((af_parity(w0&0x0071e370U)^af_parity(w1&0x0071e370U)^1U)<<28U)|((af_parity(w0&0x00e3c6e0U)^af_parity(w1&0x00e3c6e0U)^1U)<<29U)|((af_parity(w0&0x00c35cc0U)^af_parity(w1&0x00c35cc0U)^1U)<<30U)|((af_parity(w0&0x00826880U)^af_parity(w1&0x00826880U)^1U)<<31U);
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
if(cfg==4U){
uint32_t o0=((af_parity(w0&0x04d101dfU)^af_parity(w1&0x04d101dfU))<<0U)|((af_parity(w0&0x09a203beU)^af_parity(w1&0x09a203beU))<<1U)|((af_parity(w0&0x1344077dU)^af_parity(w1&0x1344077dU)^1U)<<2U)|((af_parity(w0&0x26880efaU)^af_parity(w1&0x26880efaU)^1U)<<3U)|((af_parity(w0&0x4d101df4U)^af_parity(w1&0x4d101df4U)^1U)<<4U)|((af_parity(w0&0x9a203be9U)^af_parity(w1&0x9a203be9U))<<5U)|((af_parity(w0&0x3091760dU)^af_parity(w1&0x3091760dU))<<6U)|((af_parity(w0&0x6122ec1aU)^af_parity(w1&0x6122ec1aU))<<7U)|((af_parity(w0&0xc245d835U)^af_parity(w1&0xc245d835U)^1U)<<8U)|((af_parity(w0&0x805ab1b5U)^af_parity(w1&0x805ab1b5U)^1U)<<9U)|((af_parity(w0&0x046462b5U)^af_parity(w1&0x046462b5U)^1U)<<10U)|((af_parity(w0&0x08c8c56aU)^af_parity(w1&0x08c8c56aU)^1U)<<11U)|((af_parity(w0&0x11918ad4U)^af_parity(w1&0x11918ad4U)^1U)<<12U)|((af_parity(w0&0x232315a9U)^af_parity(w1&0x232315a9U))<<13U)|((af_parity(w0&0x46462b53U)^af_parity(w1&0x46462b53U)^1U)<<14U)|((af_parity(w0&0x8c8c56a6U)^af_parity(w1&0x8c8c56a6U)^1U)<<15U)|((af_parity(w0&0x1dc9ac92U)^af_parity(w1&0x1dc9ac92U))<<16U)|((af_parity(w0&0x3b935924U)^af_parity(w1&0x3b935924U))<<17U)|((af_parity(w0&0x7726b249U)^af_parity(w1&0x7726b249U)^1U)<<18U)|((af_parity(w0&0xee4d6493U)^af_parity(w1&0xee4d6493U))<<19U)|((af_parity(w0&0xd84bc8f9U)^af_parity(w1&0xd84bc8f9U))<<20U)|((af_parity(w0&0xb446902dU)^af_parity(w1&0xb446902dU))<<21U)|((af_parity(w0&0x6c5c2184U)^af_parity(w1&0x6c5c2184U)^1U)<<22U)|((af_parity(w0&0xd8b84309U)^af_parity(w1&0xd8b84309U))<<23U)|((af_parity(w0&0xb5a187ccU)^af_parity(w1&0xb5a187ccU)^1U)<<24U)|((af_parity(w0&0x6f920e46U)^af_parity(w1&0x6f920e46U))<<25U)|((af_parity(w0&0xdf241c8cU)^af_parity(w1&0xdf241c8cU))<<26U)|((af_parity(w0&0xba9938c7U)^af_parity(w1&0xba9938c7U))<<27U)|((af_parity(w0&0x71e37051U)^af_parity(w1&0x71e37051U))<<28U)|((af_parity(w0&0xe3c6e0a3U)^af_parity(w1&0xe3c6e0a3U)^1U)<<29U)|((af_parity(w0&0xc35cc098U)^af_parity(w1&0xc35cc098U))<<30U)|((af_parity(w0&0x826880efU)^af_parity(w1&0x826880efU))<<31U);
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
if(cfg==5U){
uint32_t o0=((af_parity(w0&0xd101df48U)^af_parity(w1&0xd101df48U)^af_parity(w2&0x00000004U)^1U)<<0U)|((af_parity(w0&0xa203be90U)^af_parity(w1&0xa203be90U)^af_parity(w2&0x00000009U))<<1U)|((af_parity(w0&0x44077d20U)^af_parity(w1&0x44077d20U)^af_parity(w2&0x00000013U)^1U)<<2U)|((af_parity(w0&0x880efa40U)^af_parity(w1&0x880efa40U)^af_parity(w2&0x00000026U)^1U)<<3U)|((af_parity(w0&0x101df481U)^af_parity(w1&0x101df481U)^af_parity(w2&0x0000004dU)^1U)<<4U)|((af_parity(w0&0x203be903U)^af_parity(w1&0x203be903U)^af_parity(w2&0x0000009aU))<<5U)|((af_parity(w0&0x91760d4eU)^af_parity(w1&0x91760d4eU)^af_parity(w2&0x00000030U))<<6U)|((af_parity(w0&0x22ec1a9dU)^af_parity(w1&0x22ec1a9dU)^af_parity(w2&0x00000061U))<<7U)|((af_parity(w0&0x45d8353bU)^af_parity(w1&0x45d8353bU)^af_parity(w2&0x000000c2U)^1U)<<8U)|((af_parity(w0&0x5ab1b53eU)^af_parity(w1&0x5ab1b53eU)^af_parity(w2&0x00000080U)^1U)<<9U)|((af_parity(w0&0x6462b534U)^af_parity(w1&0x6462b534U)^af_parity(w2&0x00000004U)^1U)<<10U)|((af_parity(w0&0xc8c56a69U)^af_parity(w1&0xc8c56a69U)^af_parity(w2&0x00000008U))<<11U)|((af_parity(w0&0x918ad4d2U)^af_parity(w1&0x918ad4d2U)^af_parity(w2&0x00000011U)^1U)<<12U)|((af_parity(w0&0x2315a9a5U)^af_parity(w1&0x2315a9a5U)^af_parity(w2&0x00000023U)^1U)<<13U)|((af_parity(w0&0x462b534aU)^af_parity(w1&0x462b534aU)^af_parity(w2&0x00000046U)^1U)<<14U)|((af_parity(w0&0x8c56a694U)^af_parity(w1&0x8c56a694U)^af_parity(w2&0x0000008cU)^1U)<<15U)|((af_parity(w0&0xc9ac9260U)^af_parity(w1&0xc9ac9260U)^af_parity(w2&0x0000001dU))<<16U)|((af_parity(w0&0x935924c0U)^af_parity(w1&0x935924c0U)^af_parity(w2&0x0000003bU)^1U)<<17U)|((af_parity(w0&0x26b24980U)^af_parity(w1&0x26b24980U)^af_parity(w2&0x00000077U))<<18U)|((af_parity(w0&0x4d649300U)^af_parity(w1&0x4d649300U)^af_parity(w2&0x000000eeU))<<19U)|((af_parity(w0&0x4bc8f948U)^af_parity(w1&0x4bc8f948U)^af_parity(w2&0x000000d8U))<<20U)|((af_parity(w0&0x46902dd9U)^af_parity(w1&0x46902dd9U)^af_parity(w2&0x000000b4U)^1U)<<21U)|((af_parity(w0&0x5c2184fbU)^af_parity(w1&0x5c2184fbU)^af_parity(w2&0x0000006cU))<<22U)|((af_parity(w0&0xb84309f6U)^af_parity(w1&0xb84309f6U)^af_parity(w2&0x000000d8U))<<23U)|((af_parity(w0&0xa187cca5U)^af_parity(w1&0xa187cca5U)^af_parity(w2&0x000000b5U))<<24U)|((af_parity(w0&0x920e4602U)^af_parity(w1&0x920e4602U)^af_parity(w2&0x0000006fU)^1U)<<25U)|((af_parity(w0&0x241c8c05U)^af_parity(w1&0x241c8c05U)^af_parity(w2&0x000000dfU)^1U)<<26U)|((af_parity(w0&0x9938c743U)^af_parity(w1&0x9938c743U)^af_parity(w2&0x000000baU))<<27U)|((af_parity(w0&0xe37051cfU)^af_parity(w1&0xe37051cfU)^af_parity(w2&0x00000071U))<<28U)|((af_parity(w0&0xc6e0a39fU)^af_parity(w1&0xc6e0a39fU)^af_parity(w2&0x000000e3U))<<29U)|((af_parity(w0&0x5cc09876U)^af_parity(w1&0x5cc09876U)^af_parity(w2&0x000000c3U)^1U)<<30U)|((af_parity(w0&0x6880efa4U)^af_parity(w1&0x6880efa4U)^af_parity(w2&0x00000082U)^1U)<<31U);
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
uint32_t o0=((af_parity(w0&0x01df481bU)^af_parity(w1&0x01df481bU)^af_parity(w2&0x000004d1U)^1U)<<0U)|((af_parity(w0&0x03be9036U)^af_parity(w1&0x03be9036U)^af_parity(w2&0x000009a2U)^1U)<<1U)|((af_parity(w0&0x077d206dU)^af_parity(w1&0x077d206dU)^af_parity(w2&0x00001344U))<<2U)|((af_parity(w0&0x0efa40daU)^af_parity(w1&0x0efa40daU)^af_parity(w2&0x00002688U))<<3U)|((af_parity(w0&0x1df481b4U)^af_parity(w1&0x1df481b4U)^af_parity(w2&0x00004d10U))<<4U)|((af_parity(w0&0x3be90369U)^af_parity(w1&0x3be90369U)^af_parity(w2&0x00009a20U)^1U)<<5U)|((af_parity(w0&0x760d4ec8U)^af_parity(w1&0x760d4ec8U)^af_parity(w2&0x00003091U))<<6U)|((af_parity(w0&0xec1a9d91U)^af_parity(w1&0xec1a9d91U)^af_parity(w2&0x00006122U)^1U)<<7U)|((af_parity(w0&0xd8353b23U)^af_parity(w1&0xd8353b23U)^af_parity(w2&0x0000c245U)^1U)<<8U)|((af_parity(w0&0xb1b53e5dU)^af_parity(w1&0xb1b53e5dU)^af_parity(w2&0x0000805aU))<<9U)|((af_parity(w0&0x62b534a0U)^af_parity(w1&0x62b534a0U)^af_parity(w2&0x00000464U))<<10U)|((af_parity(w0&0xc56a6940U)^af_parity(w1&0xc56a6940U)^af_parity(w2&0x000008c8U))<<11U)|((af_parity(w0&0x8ad4d281U)^af_parity(w1&0x8ad4d281U)^af_parity(w2&0x00001191U))<<12U)|((af_parity(w0&0x15a9a502U)^af_parity(w1&0x15a9a502U)^af_parity(w2&0x00002323U)^1U)<<13U)|((af_parity(w0&0x2b534a05U)^af_parity(w1&0x2b534a05U)^af_parity(w2&0x00004646U))<<14U)|((af_parity(w0&0x56a6940bU)^af_parity(w1&0x56a6940bU)^af_parity(w2&0x00008c8cU)^1U)<<15U)|((af_parity(w0&0xac92600cU)^af_parity(w1&0xac92600cU)^af_parity(w2&0x00001dc9U))<<16U)|((af_parity(w0&0x5924c018U)^af_parity(w1&0x5924c018U)^af_parity(w2&0x00003b93U)^1U)<<17U)|((af_parity(w0&0xb2498031U)^af_parity(w1&0xb2498031U)^af_parity(w2&0x00007726U))<<18U)|((af_parity(w0&0x64930063U)^af_parity(w1&0x64930063U)^af_parity(w2&0x0000ee4dU))<<19U)|((af_parity(w0&0xc8f948ddU)^af_parity(w1&0xc8f948ddU)^af_parity(w2&0x0000d84bU))<<20U)|((af_parity(w0&0x902dd9a0U)^af_parity(w1&0x902dd9a0U)^af_parity(w2&0x0000b446U))<<21U)|((af_parity(w0&0x2184fb5bU)^af_parity(w1&0x2184fb5bU)^af_parity(w2&0x00006c5cU)^1U)<<22U)|((af_parity(w0&0x4309f6b6U)^af_parity(w1&0x4309f6b6U)^af_parity(w2&0x0000d8b8U)^1U)<<23U)|((af_parity(w0&0x87cca577U)^af_parity(w1&0x87cca577U)^af_parity(w2&0x0000b5a1U)^1U)<<24U)|((af_parity(w0&0x0e4602f5U)^af_parity(w1&0x0e4602f5U)^af_parity(w2&0x00006f92U))<<25U)|((af_parity(w0&0x1c8c05eaU)^af_parity(w1&0x1c8c05eaU)^af_parity(w2&0x0000df24U))<<26U)|((af_parity(w0&0x38c743cfU)^af_parity(w1&0x38c743cfU)^af_parity(w2&0x0000ba99U))<<27U)|((af_parity(w0&0x7051cf84U)^af_parity(w1&0x7051cf84U)^af_parity(w2&0x000071e3U)^1U)<<28U)|((af_parity(w0&0xe0a39f08U)^af_parity(w1&0xe0a39f08U)^af_parity(w2&0x0000e3c6U)^1U)<<29U)|((af_parity(w0&0xc098760bU)^af_parity(w1&0xc098760bU)^af_parity(w2&0x0000c35cU))<<30U)|((af_parity(w0&0x80efa40dU)^af_parity(w1&0x80efa40dU)^af_parity(w2&0x00008268U)^1U)<<31U);
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
if(cfg==7U){
uint32_t o0=((af_parity(w0&0xdf481b4eU)^af_parity(w1&0xdf481b4eU)^af_parity(w2&0x0004d101U))<<0U)|((af_parity(w0&0xbe90369cU)^af_parity(w1&0xbe90369cU)^af_parity(w2&0x0009a203U)^1U)<<1U)|((af_parity(w0&0x7d206d39U)^af_parity(w1&0x7d206d39U)^af_parity(w2&0x00134407U)^1U)<<2U)|((af_parity(w0&0xfa40da72U)^af_parity(w1&0xfa40da72U)^af_parity(w2&0x0026880eU)^1U)<<3U)|((af_parity(w0&0xf481b4e5U)^af_parity(w1&0xf481b4e5U)^af_parity(w2&0x004d101dU)^1U)<<4U)|((af_parity(w0&0xe90369cbU)^af_parity(w1&0xe90369cbU)^af_parity(w2&0x009a203bU)^1U)<<5U)|((af_parity(w0&0x0d4ec8d8U)^af_parity(w1&0x0d4ec8d8U)^af_parity(w2&0x00309176U)^1U)<<6U)|((af_parity(w0&0x1a9d91b1U)^af_parity(w1&0x1a9d91b1U)^af_parity(w2&0x006122ecU))<<7U)|((af_parity(w0&0x353b2363U)^af_parity(w1&0x353b2363U)^af_parity(w2&0x00c245d8U)^1U)<<8U)|((af_parity(w0&0xb53e5d89U)^af_parity(w1&0xb53e5d89U)^af_parity(w2&0x00805ab1U)^1U)<<9U)|((af_parity(w0&0xb534a05cU)^af_parity(w1&0xb534a05cU)^af_parity(w2&0x00046462U)^1U)<<10U)|((af_parity(w0&0x6a6940b9U)^af_parity(w1&0x6a6940b9U)^af_parity(w2&0x0008c8c5U)^1U)<<11U)|((af_parity(w0&0xd4d28172U)^af_parity(w1&0xd4d28172U)^af_parity(w2&0x0011918aU)^1U)<<12U)|((af_parity(w0&0xa9a502e4U)^af_parity(w1&0xa9a502e4U)^af_parity(w2&0x00232315U))<<13U)|((af_parity(w0&0x534a05c8U)^af_parity(w1&0x534a05c8U)^af_parity(w2&0x0046462bU)^1U)<<14U)|((af_parity(w0&0xa6940b90U)^af_parity(w1&0xa6940b90U)^af_parity(w2&0x008c8c56U)^1U)<<15U)|((af_parity(w0&0x92600c6fU)^af_parity(w1&0x92600c6fU)^af_parity(w2&0x001dc9acU))<<16U)|((af_parity(w0&0x24c018dfU)^af_parity(w1&0x24c018dfU)^af_parity(w2&0x003b9359U))<<17U)|((af_parity(w0&0x498031bfU)^af_parity(w1&0x498031bfU)^af_parity(w2&0x007726b2U)^1U)<<18U)|((af_parity(w0&0x9300637eU)^af_parity(w1&0x9300637eU)^af_parity(w2&0x00ee4d64U)^1U)<<19U)|((af_parity(w0&0xf948ddb3U)^af_parity(w1&0xf948ddb3U)^af_parity(w2&0x00d84bc8U))<<20U)|((af_parity(w0&0x2dd9a029U)^af_parity(w1&0x2dd9a029U)^af_parity(w2&0x00b44690U)^1U)<<21U)|((af_parity(w0&0x84fb5b1dU)^af_parity(w1&0x84fb5b1dU)^af_parity(w2&0x006c5c21U)^1U)<<22U)|((af_parity(w0&0x09f6b63aU)^af_parity(w1&0x09f6b63aU)^af_parity(w2&0x00d8b843U))<<23U)|((af_parity(w0&0xcca5773aU)^af_parity(w1&0xcca5773aU)^af_parity(w2&0x00b5a187U)^1U)<<24U)|((af_parity(w0&0x4602f53bU)^af_parity(w1&0x4602f53bU)^af_parity(w2&0x006f920eU))<<25U)|((af_parity(w0&0x8c05ea77U)^af_parity(w1&0x8c05ea77U)^af_parity(w2&0x00df241cU)^1U)<<26U)|((af_parity(w0&0xc743cfa0U)^af_parity(w1&0xc743cfa0U)^af_parity(w2&0x00ba9938U)^1U)<<27U)|((af_parity(w0&0x51cf840eU)^af_parity(w1&0x51cf840eU)^af_parity(w2&0x0071e370U)^1U)<<28U)|((af_parity(w0&0xa39f081dU)^af_parity(w1&0xa39f081dU)^af_parity(w2&0x00e3c6e0U))<<29U)|((af_parity(w0&0x98760b74U)^af_parity(w1&0x98760b74U)^af_parity(w2&0x00c35cc0U))<<30U)|((af_parity(w0&0xefa40da7U)^af_parity(w1&0xefa40da7U)^af_parity(w2&0x00826880U)^1U)<<31U);
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
if(cfg==8U){
uint32_t o0=((af_parity(w0&0x481b4e5aU)^af_parity(w1&0x481b4e5aU)^af_parity(w2&0x04d101dfU)^1U)<<0U)|((af_parity(w0&0x90369cb5U)^af_parity(w1&0x90369cb5U)^af_parity(w2&0x09a203beU))<<1U)|((af_parity(w0&0x206d396bU)^af_parity(w1&0x206d396bU)^af_parity(w2&0x1344077dU))<<2U)|((af_parity(w0&0x40da72d7U)^af_parity(w1&0x40da72d7U)^af_parity(w2&0x26880efaU)^1U)<<3U)|((af_parity(w0&0x81b4e5afU)^af_parity(w1&0x81b4e5afU)^af_parity(w2&0x4d101df4U))<<4U)|((af_parity(w0&0x0369cb5eU)^af_parity(w1&0x0369cb5eU)^af_parity(w2&0x9a203be9U)^1U)<<5U)|((af_parity(w0&0x4ec8d8e6U)^af_parity(w1&0x4ec8d8e6U)^af_parity(w2&0x3091760dU)^1U)<<6U)|((af_parity(w0&0x9d91b1cdU)^af_parity(w1&0x9d91b1cdU)^af_parity(w2&0x6122ec1aU))<<7U)|((af_parity(w0&0x3b23639aU)^af_parity(w1&0x3b23639aU)^af_parity(w2&0xc245d835U)^1U)<<8U)|((af_parity(w0&0x3e5d896eU)^af_parity(w1&0x3e5d896eU)^af_parity(w2&0x805ab1b5U)^1U)<<9U)|((af_parity(w0&0x34a05c86U)^af_parity(w1&0x34a05c86U)^af_parity(w2&0x046462b5U)^1U)<<10U)|((af_parity(w0&0x6940b90cU)^af_parity(w1&0x6940b90cU)^af_parity(w2&0x08c8c56aU)^1U)<<11U)|((af_parity(w0&0xd2817218U)^af_parity(w1&0xd2817218U)^af_parity(w2&0x11918ad4U)^1U)<<12U)|((af_parity(w0&0xa502e430U)^af_parity(w1&0xa502e430U)^af_parity(w2&0x232315a9U))<<13U)|((af_parity(w0&0x4a05c860U)^af_parity(w1&0x4a05c860U)^af_parity(w2&0x46462b53U)^1U)<<14U)|((af_parity(w0&0x940b90c0U)^af_parity(w1&0x940b90c0U)^af_parity(w2&0x8c8c56a6U)^1U)<<15U)|((af_parity(w0&0x600c6fdaU)^af_parity(w1&0x600c6fdaU)^af_parity(w2&0x1dc9ac92U))<<16U)|((af_parity(w0&0xc018dfb5U)^af_parity(w1&0xc018dfb5U)^af_parity(w2&0x3b935924U)^1U)<<17U)|((af_parity(w0&0x8031bf6aU)^af_parity(w1&0x8031bf6aU)^af_parity(w2&0x7726b249U))<<18U)|((af_parity(w0&0x00637ed5U)^af_parity(w1&0x00637ed5U)^af_parity(w2&0xee4d6493U))<<19U)|((af_parity(w0&0x48ddb3f0U)^af_parity(w1&0x48ddb3f0U)^af_parity(w2&0xd84bc8f9U))<<20U)|((af_parity(w0&0xd9a029bbU)^af_parity(w1&0xd9a029bbU)^af_parity(w2&0xb446902dU)^1U)<<21U)|((af_parity(w0&0xfb5b1d2cU)^af_parity(w1&0xfb5b1d2cU)^af_parity(w2&0x6c5c2184U))<<22U)|((af_parity(w0&0xf6b63a59U)^af_parity(w1&0xf6b63a59U)^af_parity(w2&0xd8b84309U))<<23U)|((af_parity(w0&0xa5773ae8U)^af_parity(w1&0xa5773ae8U)^af_parity(w2&0xb5a187ccU)^1U)<<24U)|((af_parity(w0&0x02f53b8aU)^af_parity(w1&0x02f53b8aU)^af_parity(w2&0x6f920e46U))<<25U)|((af_parity(w0&0x05ea7715U)^af_parity(w1&0x05ea7715U)^af_parity(w2&0xdf241c8cU)^1U)<<26U)|((af_parity(w0&0x43cfa071U)^af_parity(w1&0x43cfa071U)^af_parity(w2&0xba9938c7U))<<27U)|((af_parity(w0&0xcf840eb8U)^af_parity(w1&0xcf840eb8U)^af_parity(w2&0x71e37051U))<<28U)|((af_parity(w0&0x9f081d70U)^af_parity(w1&0x9f081d70U)^af_parity(w2&0xe3c6e0a3U)^1U)<<29U)|((af_parity(w0&0x760b74bbU)^af_parity(w1&0x760b74bbU)^af_parity(w2&0xc35cc098U)^1U)<<30U)|((af_parity(w0&0xa40da72dU)^af_parity(w1&0xa40da72dU)^af_parity(w2&0x826880efU))<<31U);
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
