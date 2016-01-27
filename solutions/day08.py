import re

input = [r'"azlgxdbljwygyttzkfwuxv"',r'"v\xfb\"lgs\"kvjfywmut\x9cr"',r'"merxdhj"',r'"dwz"',r'"d\\gkbqo\\fwukyxab\"u"',r'"k\xd4cfixejvkicryipucwurq\x7eq"',r'"nvtidemacj\"hppfopvpr"',r'"kbngyfvvsdismznhar\\p\"\"gpryt\"jaeh"',r'"khre\"o\x0elqfrbktzn"',r'"nugkdmqwdq\x50amallrskmrxoyo"',r'"jcrkptrsasjp\\\"cwigzynjgspxxv\\vyb"',r'"ramf\"skhcmenhbpujbqwkltmplxygfcy"',r'"aqjqgbfqaxga\\fkdcahlfi\"pvods"',r'"pcrtfb"',r'"\x83qg\"nwgugfmfpzlrvty\"ryoxm"',r'"fvhvvokdnl\\eap"',r'"kugdkrat"',r'"seuxwc"',r'"vhioftcosshaqtnz"',r'"gzkxqrdq\\uko\"mrtst"',r'"znjcomvy\x16hhsenmroswr"',r'"clowmtra"',r'"\xc4"',r'"jpavsevmziklydtqqm"',r'"egxjqytcttr\\ecfedmmovkyn\"m"',r'"mjulrvqgmsvmwf"',r'"o\\prxtlfbatxerhev\xf9hcl\x44rzmvklviv"',r'"lregjexqaqgwloydxdsc\\o\"dnjfmjcu"',r'"lnxluajtk\x8desue\\k\x7abhwokfhh"',r'"wrssfvzzn\"llrysjgiu\"npjtdli"',r'"\x67lwkks"',r'"bifw\"ybvmwiyi\"vhol\"vol\xd4"',r'"aywdqhvtvcpvbewtwuyxrix"',r'"gc\xd3\"caukdgfdywj"',r'"uczy\\fk"',r'"bnlxkjvl\x7docehufkj\\\"qoyhag"',r'"bidsptalmoicyorbv\\"',r'"jorscv\"mufcvvfmcv\"ga"',r'"sofpwfal\\a"',r'"kcuqtbboaly\"uj\"k"',r'"n\\c"',r'"x\"\xcaj\\xwwvpdldz"',r'"eyukphh"',r'"wcyjq"',r'"vjx\"\"hjroj\"l\x4cjwbr"',r'"xcodsxzfqw\\rowqtuwvjnxupjnrh"',r'"yc"',r'"fpvzldgbdtca\"hqwa"',r'"ymjq\x8ahohvafubra\"hgqoknkuyph"',r'"kx\\mkaaklvcup"',r'"belddrzegcsxsyfhzyz"',r'"fuyswi"',r'"\\hubzebo\"ha\\qyr\"dv\\"',r'"mxvlz\"fwuvx\"cyk\""',r'"ftbh\"ro\\tmcpnpvh\"xx"',r'"ygi"',r'"rw\"\"wwn\\fgbjumq\"vgvoh\xd0\"mm"',r'"\"pat\"\x63kpfc\"\x2ckhfvxk\"uwqzlx"',r'"o"',r'"d\"hqtsfp\xceaswe\"\xc0lw"',r'"zajpvfawqntvoveal\"\"trcdarjua"',r'"xzapq"',r'"rkmhm"',r'"byuq"',r'"rwwmt\xe8jg\xc2\"omt"',r'"nfljgdmgefvlh\"x"',r'"rpjxcexisualz"',r'"doxcycmgaiptvd"',r'"rq\\\"mohnjdf\\xv\\hrnosdtmvxot"',r'"oqvbcenib\"uhy\\npjxg"',r'"pkvgnm\\ruayuvpbpd"',r'"kknmzpxqfbcdgng"',r'"piduhbmaympxdexz"',r'"vapczawekhoa\\or"',r'"tlwn\"avc\"bycg\"\"xuxea"',r'"\xcdvryveteqzxrgopmdmihkcgsuozips"',r'"kpzziqt"',r'"sdy\\s\"cjq"',r'"yujs"',r'"qte\"q"',r'"qyvpnkhjcqjv\"cclvv\"pclgtg\xeak\"tno"',r'"xwx"',r'"vibuvv"',r'"qq\""',r'"wwjduomtbkbdtorhpyalxswisq\"r"',r'"afuw\\mfjzctcivwesutxbk\"lk"',r'"e\xcef\\hkiu"',r'"ftdrgzvygcw\"jwsrcmgxj"',r'"zrddqfkx\x21dr\"ju\"elybk\"powj\"\"kpryz"',r'"dttdkfvbodkma\""',r'"lzygktugpqw"',r'"qu\x83tes\\u\"tnid\"ryuz"',r'"\\o\"pe\\vqwlsizjklwrjofg\xe2oau\\rd"',r'"mikevjzhnwgx\"fozrj\"h\""',r'"ligxmxznzvtachvvbahnff"',r'"d\\kq"',r'"tnbkxpzmcakqhaa"',r'"g\\yeakebeyv"',r'"cqkcnd\"sxjxfnawy\x31zax\x6ceha"',r'"m\x0dtqotffzdnetujtsgjqgwddc"',r'"masnugb\"etgmxul\x3bqd\\tmtddnvcy"',r'"floediikodfgre\x23wyoxlswxflwecdjpt"',r'"zu"',r'"r"',r'"\"ashzdbd\"pdvba\xeeumkr\\amnj"',r'"ckslmuwbtfouwpfwtuiqmeozgspwnhx"',r'"t\\qjsjek\xf9gjcxsyco\"r"',r'"hoed\x1b\\tcmaqch\"epdy"',r'"mgjiojwzc\\ypqcn\xb1njmp\"aeeblxt"',r'"\xdf\"h\x5enfracj"',r'"\x6fpbpocrb"',r'"jbmhrswyyq\\"',r'"wtyqtenfwatji\"ls\\"',r'"voy"',r'"awj"',r'"rtbj\"j"',r'"hynl"',r'"orqqeuaat\\xu\\havsgr\xc5qdk"',r'"g\"npyzjfq\"rjefwsk"',r'"rk\\kkcirjbixr\\zelndx\"bsnqvqj\""',r'"tecoz"',r'"dn\"uswngbdk\""',r'"qb\\"',r'"wpyis\\ebq"',r'"ppwue\\airoxzjjdqbvyurhaabetv"',r'"fxlvt"',r'"ql\"oqsmsvpxcg\"k"',r'"vqlhuec\\adw"',r'"qzmi\xffberakqqkk"',r'"tisjqff\"wf"',r'"yhnpudoaybwucvppj"',r'"xhfuf\\ehsrhsnfxcwtibd\"ubfpz"',r'"ihgjquzhf\""',r'"ff\x66dsupesrnusrtqnywoqcn\\"',r'"z\x77zpubbjmd"',r'"\"vhzlbwq\"xeimjt\\xe\x85umho\"m\"\"bmy"',r'"mmuvkioocmzjjysi\"mkfbec\""',r'"rpgghowbduw\x2fayslubajinoik\xd0hcfy"',r'"xrkyjqul\xdexlojgdphczp\"jfk"',r'"mg\x07cnr\x8b\x67xdgszmgiktpjhawho"',r'"kdgufhaoab"',r'"rlhela\"nldr"',r'"wzye\x87u"',r'"yif\x75bjhnitgoarmfgqwpmopu"',r'"pvlbyez\"wyy\x3dpgr"',r'"ezdm\"ovkruthkvdwtqwr\"ibdoawzgu"',r'"qubp"',r'"b\\kcpegcn\\zgdemgorjnk"',r'"gjsva\\kzaor\"\"gtpd"',r'"\"kt"',r'"rlymwlcodix"',r'"qqtmswowxca\"jvv"',r'"jni\xebwhozb"',r'"zhino\"kzjtmgxpi\"zzexijg"',r'"tyrbat\\mejgzplufxixkyg"',r'"lhmopxiao\x09\"p\xebl"',r'"xefioorxvate"',r'"nmcgd\x46xfujt\"w"',r'"\xe3wnwpat\"gtimrb"',r'"wpq\"xkjuw\xebbohgcagppb"',r'"fmvpwaca"',r'"mlsw"',r'"fdan\\\x9e"',r'"\"f\"fmdlzc"',r'"nyuj\\jnnfzdnrqmhvjrahlvzl"',r'"zn\"f\xcfsshcdaukkimfwk"',r'"uayugezzo\\\"e\"blnrgjaupqhik"',r'"efd\"apkndelkuvfvwyyatyttkehc"',r'"ufxq\\\"m\"bwkh\x93kapbqrvxxzbzp\\"',r'"fgypsbgjak\x79qblbeidavqtddfacq\\i\"h"',r'"kcfgpiysdxlgejjvgndb\\dovfpqodw"',r'"\"onpqnssmighipuqgwx\"nrokzgvg"',r'"vhjrrhfrba\"jebdanzsrdusut\\wbs"',r'"o\xdakymbaxakys"',r'"uwxhhzz\\mtmhghjn\\\\tnhzbejj"',r'"yd\\"',r'"bpgztp\\lzwpdqju\"it\x35qjhihjv"',r'"\\my\\b\"klnnto\\\xb3mbtsh"',r'"ezyvknv\"l\x2bdhhfjcvwzhjgmhwbqd\"\\"',r'"ftkz\"amoncbsohtaumhl\"wsodemopodq"',r'"ifv"',r'"dmzfxvzq"',r'"sped\"bvmf\"mmevl\"zydannpfny"',r'"fjxcjwlv\"pnqyrzatsjwsqfidb"',r'"muc\xfdqouwwnmuixru\\zlhjintplvtee"',r'"mraqgvmj"',r'"njopq\"ftcsryo"',r'"enoh\"n"',r'"t\"ntjhjc\"nzqh\xf7dcohhlsja\x7dtr"',r'"flbqcmcoun"',r'"dxkiysrn\\dyuqoaig"',r'"nehkzi\"h\"syktzfufotng\xdafqo"',r'"dzkjg\\hqjk\\\"zfegssjhn"',r'"sadlsjv"',r'"vmfnrdb\""',r'"ac\\bdp\"n"',r'"qt\x89h"',r'"lsndeugwvijwde\\vjapbm\\k\\nljuva"',r'"twpmltdzyynqt\\z\\tnund\x64hm"',r'"hpcyata\"ocylbkzdnhujh"',r'"hskzq\"knntuhscex\"q\\y\\vqj\x3an"',r'"eekwyufvji\\mqgeroekxeyrmymq"',r'"hl\"durthetvri\xebw\\jxu\"rcmiuy"',r'"\"fxdnmvnftxwesmvvq\"sjnf\xaabpg\"iary"',r'"\"\"nksqso"',r'"ruq\xbezugge\"d\"hwvoxmy\"iawikddxn\"x"',r'"rxxnlfay"',r'"stcu\"mv\xabcqts\\fasff"',r'"yrnvwfkfuzuoysfdzl\x02bk"',r'"qbdsmlwdbfknivtwijbwtatqfe"',r'"\"erqh\\csjph"',r'"ikfv"',r'"\xd2cuhowmtsxepzsivsvnvsb"',r'"vj"',r'"d"',r'"\\g"',r'"porvg\x62qghorthnc\"\\"',r'"tiks\\kr\"\x0fuejvuxzswnwdjscrk"',r'"xmgfel\"atma\\zaxmlgfjx\"ajmqf"',r'"oz\\rnxwljc\\\"umhymtwh"',r'"wlsxxhm\x7fqx\\gjoyrvccfiner\\qloluqv"',r'"k\\ieq"',r'"xidjj\"ksnlgnwxlddf\\s\\kuuleb"',r'"wjpnzgprzv\\maub\x0cj"',r'"r"',r'"y"',r'"\"yecqiei\"ire\\jdhlnnlde\xc5u"',r'"drvdiycqib"',r'"egnrbefezcrhgldrtb"',r'"plqodxv\\zm\"uodwjdocri\x55ucaezutm"',r'"f\"wexcw\x02ekewx\"alyzn"',r'"pqajwuk\\\\oatkfqdyspnrupo"',r'"rkczj\"fzntabpnygrhamk\\km\x68xfkmr"',r'"wejam\xbac\x37kns"',r'"qqmlwjk\"gh"',r'"fdcjsxlgx"',r'"\\cxvxy\"kb\"\"unubvrsq\\y\\awfhbmarj\\"',r'"geunceaqr"',r'"tpkg\"svvngk\\sizlsyaqwf"',r'"\"pa\\x\x18od\\emgje\\"',r'"ffiizogjjptubzqfuh\"cctieqcdh"',r'"yikhiyyrpgglpos"',r'"h\\"',r'"jotqojodcv"',r'"ervsz\x87ade\"fevq\\tcqowt"',r'"\\y\"fgrxtppkcseeg\\onxjarx\\hyhfn\x5fi"',r'"kxndlabn\\wwumctuzdcfiitrbnn"',r'"eoosynwhwm"',r'"\"c\x04"',r'"ny\xf6vuwlec"',r'"ubgxxcvnltzaucrzg\\xcez"',r'"pnocjvo\\yt"',r'"fcabrtqog\"a\"zj"',r'"o\\bha\\mzxmrfltnflv\xea"',r'"tbfvzwhexsdxjmxejwqqngzixcx"',r'"wdptrakok\"rgymturdmwfiwu"',r'"reffmj"',r'"lqm"',r'"\\oc"',r'"p\""',r'"ygkdnhcuehlx"',r'"vsqmv\"bqay\"olimtkewedzm"',r'"isos\x6azbnkojhxoopzetbj\xe1yd"',r'"yo\\pgayjcyhshztnbdv"',r'"fg\"h"',r'"vcmcojolfcf\\\\oxveua"',r'"w\"vyszhbrr\"jpeddpnrjlca\x69bdbopd\\z"',r'"jikeqv"',r'"\"dkjdfrtj"',r'"is"',r'"hgzx"',r'"z\""',r'"woubquq\\ag\""',r'"xvclriqa\xe6ltt"',r'"tfxinifmd"',r'"mvywzf\"jz"',r'"vlle"',r'"c\"rf\"wynhye\x25vccvb\""',r'"zvuxm"',r'"\xf2\"jdstiwqer\"h"',r'"kyogyogcknbzv\x9f\\\\e"',r'"kspodj\"edpeqgypc"',r'"oh\\x\\h"',r'"julb"',r'"bmcfkidxyilgoy\\xmu\"ig\\qg"',r'"veqww\"ea"',r'"fkdbemtgtkpqisrwlxutllxc\"mbelhs"',r'"e"',r'"ecn\x50ooprbstnq"',r'"\"\xe8\"ec\xeah\"qo\\g\"iuqxy\"e\"y\xe7xk\xc6d"',r'"lwj\"aftrcqj"',r'"jduij\x97zk\"rftjrixzgscxxllpqx\"bwwb"',r'"fqcditz"',r'"f\x19azclj\"rsvaokgvty\"aeq"',r'"erse\x9etmzhlmhy\x67yftoti"',r'"lsdw\xb3dmiy\\od"',r'"x\x6fxbljsjdgd\xaau"',r'"hjg\\w\"\x78uoqbsdikbjxpip\"w\"jnhzec"',r'"gk"',r'"\\zrs\\syur"']

class Day08(object):
    def __init__(self):
        self.state = 0
        self.code_character_count = 0
        self.in_memory_character_count = 0

    def part_one(self, input):
        for s in input:
            print s
            self.code_character_count += len(s)
            self.state = 0

            # 0 : start state
            # 1 : string state
            # 2 : escape state
            # 3 : hexadecimal state
            hex_read = 0
            for c in s:
                if c == '\\':
                    character = 'escape'
                elif c == '"':
                    character = 'double-quote'
                elif c == 'x':
                    character = 'x'
                elif re.match('\d', c):
                    character = 'number'
                elif re.match('[a-z]', c):
                    character = 'character'
                else:
                    raise Exception('unknown character ' + str(c))

                if self.state == 0:
                    # regular character state : no increment, should only change to string state
                    if character in ['double-quote']:
                        self.state = 1
                    else:
                        raise Exception('inconsistent state 0')
                elif self.state == 1:
                    # string state : increment in-memory character count when character is not escape or double quote
                    if character in ['character','number','x']:
                        self.in_memory_character_count += 1
                    elif character in ['double-quote']:
                        self.state = 0
                    elif character in ['escape']:
                        self.state = 2
                    else:
                        raise Exception('inconsistent state 1')
                elif self.state == 2:
                    # escape state : increment in-memory character count when character is not escape or double quote
                    if character in ['x']:
                        self.state = 3
                        hex_read = 0
                    elif character in ['double-quote', 'escape']:
                        self.in_memory_character_count += 1
                        self.state = 1
                    else:
                        raise Exception('inconsistent state 2')
                elif self.state == 3:
                    # hex state : increment in-memory character count when leaving this state
                    if character in ['number', 'character']:
                        self.state = 3
                        hex_read += 1

                        if hex_read >= 2:
                            self.state = 1
                            self.in_memory_character_count += 1
                    else:
                        raise Exception('inconsistent state 3')
                else:
                    raise Exception('invalid state : ' + str(self.state))
        return (self.code_character_count - self.in_memory_character_count)

    def part_two(self, input):
        for s in input:
            print s
            self.code_character_count += len(re.escape(s)) + 2
            self.in_memory_character_count += len(s)
        return (self.code_character_count - self.in_memory_character_count)