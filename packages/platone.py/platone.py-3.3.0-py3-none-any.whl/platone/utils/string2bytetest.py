from platone.utils.fvnhash import fnv1_64
from platone.param_encode import (rlp_encode,to_binary,)


# from platone.utils.encoding import (
#     str2bytes,encodeaddress,tobech32address,)

def hexstr2bytes(address: str):
    pos = 0
    len_str = len(address)
    if len_str % 2 != 0:
       return None
    len_str = round(len_str/2)
    hexa = []
    for i in range(len_str):
       s1 = address[pos:pos+2]
       if s1 == '0x' or s1 == '0X':
          pos +=2
          continue
       sv = s1
       hexa.append(sv)
       pos += 2
    return hexa
def tostring_hex(arr:list):
    arrhex=''
    if arr:
        for i in arr:
            arrhex= arrhex+i
        return arrhex
    else :
        return ''
def stringtohex(str1:bytes):
    strhex=[]
    if str1:
        for i in str1:
            strhex=strhex+[hex(i).replace('0x','')]
        return strhex
    else: return []
# uin=257
# uina=[]
# while (uin & 0xff):
#       temp=[]
#       temp=(hex(uin & 0xff)).replace('0x','')
#       if len(temp)==1:
#           temp='0'+temp
#       uina.append(temp)
#       uin=uin >> 8

data='0x0061736d0100000001470d60017f017f60027f7f0060000060017f0060037f7f7f0060047f7f7f7f0060027f7f017f60037f7f7f017f60047f7f7f7f017f60017f017e60027f7e006000017f60017e017f02a9010703656e760c706c61746f6e5f70616e6963000203656e7617706c61746f6e5f6765745f696e7075745f6c656e677468000b03656e7610706c61746f6e5f6765745f696e707574000303656e7617706c61746f6e5f6765745f73746174655f6c656e677468000603656e7610706c61746f6e5f6765745f7374617465000803656e7610706c61746f6e5f7365745f7374617465000503656e760d706c61746f6e5f72657475726e000103201f0202000704090903000300000c010a020803000001070106010104020000050405017001010105030100020608017f0141b088040b073904066d656d6f72790200115f5f7761736d5f63616c6c5f63746f727300070f5f5f66756e63735f6f6e5f65786974001606696e766f6b6500080ad02a1f040010220b940202047f017e230041d0006b22012400102210012200100922021002200141386a200141086a20022000100a22004100100b02400240200141386a100c2204500d00418008100d20045104402000100e200141386a100f10100c020b418508100d200451044020001011410247044010000b200141386a20004101100b200141386a100c2104200141386a100f210020012004370348200010100c020b418908100d2004520d002000100e200141206a100f210220012903302104200141386a10122200200410131014200020041015200028020c200041106a28020047044010000b200028020020002802041006200028020c22030440200020033602100b200210100c010b10000b1016200141d0006a24000b9b0101047f230041106b220124002001200036020c2000047f41a408200041086a2202411076220041a4082802006a220336020041a00841a008280200220420026a41076a417871220236020002400240200341107420024d044041a408200341016a360200200041016a21000c010b2000450d010b200040000d0010000b20042001410c6a4104101c41086a0541000b2100200141106a240020000b0c00200020012002411c10170bc90202067f017e230041106b220324002001280208220520024b0440200341086a2001101d20012003280208200328020c101e36020c20032001101d410021052001027f410020032802002207450d001a410020032802042208200128020c2206490d001a200820062006417f461b210420070b360210200141146a2004360200200141003602080b200141106a210603402001280214210402402005200249044020040d01410021040b200020062802002004411410171a200341106a24000f0b20032001101d41002104027f410020032802002205450d001a410020032802042208200128020c2207490d001a200820076b2104200520076a0b2105200120043602142001200536021020032006410020052004101e10252001200329030022093702102001200128020c2009422088a76a36020c2001200128020841016a22053602080c000b000bad0302057f017e20001018024002402000280204450d00200010180240200028020022012c0000220241004e044020020d010c020b200241807f460d00200241ff0171220341b7014d0440200028020441014d04401000200028020021010b20012d00010d010c020b200341bf014b0d012000280204200241ff017141ca7e6a22024d04401000200028020021010b200120026a2d0000450d010b2000280204450d0020012d000041c001490d010b10000b200010192204200028020422014b04401000200028020421010b20002802002105024002400240200104404100210320052c00002200417f4a0d01027f200041ff0171220341bf014d04404100200041ff017141b801490d011a200341c97e6a0c010b4100200041ff017141f801490d001a200341897e6a0b41016a21030c010b4101210320050d00410021000c010b41002100200320046a20014b0d0020012004490d004100210220012003490d01200320056a2102200120036b20042004417f461b22004109490d0110000c010b410021020b0340200004402000417f6a210020023100002006420886842106200241016a21020c010b0b20060b3901027e42a5c688a1c89ca7f94b210103402000300000220250450440200041016a2100200142b383808080207e20028521010c010b0b20010b0e0020001011410147044010000b0bda0101077f230041306b22052400200042d1f0fad48ae09ad34537030820004200370300200541186a1012220220002903081015200228020c200241106a28020047044010000b02400240200228020022062002280204220710032204450d002004101a21030340200120036a41003a00002004200141016a2201470d000b20062007200320011004417f460d0020002005200341016a200120036a2003417f736a100a100c3703100c010b410021040b200228020c22010440200220013602100b2004450440200020002903003703100b200541306a240020000bb40201097f230041306b22032400200341186a10122202200029030810131014200220002903081015200228020c200241106a28020047044010000b20022802042105200228020021062003101221012000290310101321074101101a220441fe013a0000200128020c200141106a28020047044010000b2001280204220841016a220920012802084b047f20012009101b20012802040520080b20012802006a20044101101c1a2001200128020441016a3602042001200441016a200720046b6a10142001200029031010150240200128020c2001280210460440200128020021000c010b100020012802002100200128020c2001280210460d0010000b20062005200020012802041005200128020c22000440200120003602100b200228020c22010440200220013602100b200341306a24000b800101047f230041106b2201240002402000280204450d0020002802002d000041c001490d00200141086a2000101d200128020c210003402000450d01200141002001280208220320032000101e22046a20034520002004497222031b3602084100200020046b20031b2100200241016a21020c000b000b200141106a240020020b2900200041003602082000420037020020004100101b200041146a41003602002000420037020c20000b7002027f017e4101210120004280015a047f41002101034020002003845045044020034238862000420888842100200141016a2101200342088821030c010b0b024020014138490d002001210203402002450d01200141016a2101200241087621020c000b000b200141016a0520010b0b13002000280208200149044020002001101b0b0bc10402057f027e024020015004402000418001101f0c010b20014280015a044020012108034020072008845045044020074238862008420888842108200241016a2102200742088821070c010b0b0240200241384f04402002210403402004044020044108762104200341016a21030c010b0b200341c9004f044010000b2000200341b77f6a41ff0171101f2000200028020420036a1020200028020420002802006a417f6a21032002210403402004450d02200320043a0000200441087621042003417f6a21030c000b000b200020024180017341ff0171101f0b2000200028020420026a1020200028020420002802006a417f6a21024200210703402001200784500d02200220013c0000200742388620014208888421012002417f6a2102200742088821070c000b000b20002001a741ff0171101f0b0340024020002802102202200028020c460d00200241786a2802004504401000200028021021020b200241786a22042004280200417f6a220336020020030d002000200436021041002104200028020422062002417c6a28020022056b2203210203402002044020024108762102200441016a21040c010b0b20004101200441016a20034138491b220220066a1020200028020020056a220620026a200620031021200341374d0440200028020020056a200341406a3a00000c020b200441084d0440200028020020056a200441776a3a0000200028020020056a20046a210203402003450d03200220033a0000200341087621032002417f6a21020c000b000510000c020b000b0b0b880101037f4190084101360200419408280200210003402000044003404198084198082802002201417f6a220236020020014101484504404190084100360200200020024102746a22004184016a280200200041046a280200110300419008410136020041940828020021000c010b0b4198084120360200419408200028020022003602000c010b0b0b730020004200370210200042ffffffff0f370208200020023602042000200136020002402003410871450d002000102320024f0d002003410471044010000c010b200042003702000b02402003411071450d002000102320024d0d0020034104710440100020000f0b200042003702000b20000b4101017f200028020445044010000b0240200028020022012d0000418101470d00200028020441014d047f100020002802000520010b2c00014100480d0010000b0bff0201037f200028020445044041000f0b2000101841012102024020002802002c00002201417f4a0d00200141ff0171220341b7014d0440200341807f6a0f0b02400240200141ff0171220141bf014d0440024020002802042201200341c97e6a22024d047f100020002802040520010b4102490d0020002802002d00010d0010000b200241054f044010000b20002802002d000145044010000b4100210241b7012101034020012003460440200241384f0d030c0405200028020020016a41ca7e6a2d00002002410874722102200141016a21010c010b000b000b200141f7014d0440200341c07e6a0f0b024020002802042201200341897e6a22024d047f100020002802040520010b4102490d0020002802002d00010d0010000b200241054f044010000b20002802002d000145044010000b4100210241f701210103402001200346044020024138490d0305200028020020016a418a7e6a2d00002002410874722102200141016a21010c010b0b0b200241ff7d490d010b10000b20020b0b002000410120001b10090b2f01017f200028020820014904402001100920002802002000280204101c210220002001360208200020023602000b0bfc0801067f03400240200020046a2105200120046a210320022004460d002003410371450d00200520032d00003a0000200441016a21040c010b0b200220046b210602402005410371220745044003402006411049450440200020046a2203200120046a2205290200370200200341086a200541086a290200370200200441106a2104200641706a21060c010b0b027f2006410871450440200120046a2103200020046a0c010b200020046a2205200120046a2204290200370200200441086a2103200541086a0b21042006410471044020042003280200360200200341046a2103200441046a21040b20064102710440200420032f00003b0000200341026a2103200441026a21040b2006410171450d01200420032d00003a000020000f0b024020064120490d002007417f6a220741024b0d00024002400240024002400240200741016b0e020102000b2005200120046a220328020022073a0000200541016a200341016a2f00003b0000200041036a2108200220046b417d6a2106034020064111490d03200420086a2203200120046a220541046a2802002202410874200741187672360200200341046a200541086a2802002207410874200241187672360200200341086a2005410c6a28020022024108742007411876723602002003410c6a200541106a2802002207410874200241187672360200200441106a2104200641706a21060c000b000b2005200120046a220328020022073a0000200541016a200341016a2d00003a0000200041026a2108200220046b417e6a2106034020064112490d03200420086a2203200120046a220541046a2802002202411074200741107672360200200341046a200541086a2802002207411074200241107672360200200341086a2005410c6a28020022024110742007411076723602002003410c6a200541106a2802002207411074200241107672360200200441106a2104200641706a21060c000b000b2005200120046a28020022073a0000200041016a21082004417f7320026a2106034020064113490d03200420086a2203200120046a220541046a2802002202411874200741087672360200200341046a200541086a2802002207411874200241087672360200200341086a2005410c6a28020022024118742007410876723602002003410c6a200541106a2802002207411874200241087672360200200441106a2104200641706a21060c000b000b200120046a41036a2103200020046a41036a21050c020b200120046a41026a2103200020046a41026a21050c010b200120046a41016a2103200020046a41016a21050b20064110710440200520032d00003a00002005200328000136000120052003290005370005200520032f000d3b000d200520032d000f3a000f200541106a2105200341106a21030b2006410871044020052003290000370000200541086a2105200341086a21030b2006410471044020052003280000360000200541046a2105200341046a21030b20064102710440200520032f00003b0000200541026a2105200341026a21030b2006410171450d00200520032d00003a00000b20000b2101017f20011019220220012802044b044010000b2000200120011024200210250b2701017f230041206b22022400200241086a200020014114101710232100200241206a240020000b3f01027f2000280204220241016a220320002802084b047f20002003101b20002802040520020b20002802006a20013a00002000200028020441016a3602040b0f0020002001101b200020013602040b8d0301037f024020002001460d00200120006b20026b410020024101746b4d0440200020012002101c1a0c010b20002001734103712103027f024020002001490440200020030d021a410021030340200120036a2105200020036a2204410371450440200220036b210241002103034020024104490d04200320046a200320056a280200360200200341046a21032002417c6a21020c000b000b20022003460d04200420052d00003a0000200341016a21030c000b000b024020030d002001417f6a21040340200020026a22034103714504402001417c6a21032000417c6a2104034020024104490d03200220046a200220036a2802003602002002417c6a21020c000b000b2002450d042003417f6a200220046a2d00003a00002002417f6a21020c000b000b2001417f6a210103402002450d03200020026a417f6a200120026a2d00003a00002002417f6a21020c000b000b200320056a2101200320046a0b210303402002450d01200320012d00003a00002002417f6a2102200341016a2103200141016a21010c000b000b0b3501017f230041106b220041b0880436020c419c08200028020c41076a417871220036020041a008200036020041a4083f003602000b2e01017f200028020445044041000f0b4101210120002802002c0000417f4c047f20001024200010196a0520010b0b5b00027f027f41002000280204450d001a410020002802002c0000417f4a0d011a20002802002d0000220041bf014d04404100200041b801490d011a200041c97e6a0c010b4100200041f801490d001a200041897e6a0b41016a0b0b5b01027f2000027f0240200128020022054504400c010b200220036a200128020422014b0d0020012002490d00410020012003490d011a200220056a2104200120026b20032003417f461b0c010b41000b360204200020043602000b0b1301004180080b0c696e697400736574006765740a'
aa=bytes("init",'utf-8')
a1=fnv1_64(aa)
xx=to_binary(1020202)
# a21=HexBytes(a1)
a2=hex(a1)
a31=hexstr2bytes(a2)
a32=rlp_encode((a31,[]))
data1 = hexstr2bytes(data)
deploydata = rlp_encode((data1, a32))
# a31=rlp_encode(a21)
a4=tostring_hex(a32)
print(a4)