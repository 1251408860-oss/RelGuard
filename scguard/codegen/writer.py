"""Current paired writer-guard emission."""

from ..models import writer


def export_guard(a, b):
    caps_a = "||".join(("ca==" + str(v) + "U" for v in a["capacities"]))
    caps_b = "||".join(("cb==" + str(v) + "U" for v in b["capacities"]))
    return (
        '/* Source identities and premises are in binding.json. Return 0 UNKNOWN,\n1 EQUAL, 2 UNEQUAL. Caller supplies valid readable eight-byte entry arrays. */\n#include <stddef.h>\n#include <stdint.h>\n#include <limits.h>\n_Static_assert(CHAR_BIT==8 && sizeof(unsigned)==4 && sizeof(int)==4,"ABI");\n'
        + writer.emit(a, "bg_old")
        + writer.emit(b, "bg_new")
        + "\nint bg_decide(unsigned xa,unsigned ca,const unsigned char *ea,\n              unsigned xb,unsigned cb,const unsigned char *eb,unsigned mask){\n if(!ea||!eb||xa>1114111U||xb>1114111U||!mask||mask>511U||!("
        + caps_a
        + ")||!("
        + caps_b
        + "))return 0;\n unsigned char a[8],b[8];for(unsigned i=0;i<8;i++){a[i]=ea[i];b[i]=eb[i];}\n int ra=bg_old(xa,ca,a),rb=bg_new(xb,cb,b);\n if((mask&1U)&&ra!=rb)return 2;\n for(unsigned i=0;i<8;i++)if((mask&(2U<<i))&&a[i]!=b[i])return 2;\n return 1;\n}\n"
    )
