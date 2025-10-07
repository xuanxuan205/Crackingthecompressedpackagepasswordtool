import zipfile
import os
import time
import threading
import itertools
import string
import inspect

# 增强的密码字典 - 大幅扩展
ENHANCED_DICTIONARY = [
    # 最常用密码
    "123456", "password", "123456789", "12345678", "12345", "qwerty", "abc123",
    "password123", "1234567", "1234567890", "admin", "letmein", "welcome",
    "monkey", "123123", "1234", "12345678910", "dragon", "baseball", "football",
    "shadow", "master", "jordan", "superman", "harley", "hunter", "buster",
    "thomas", "tigger", "robert", "soccer", "batman", "test", "pass", "kelly",
    "hockey", "george", "charlie", "andrew", "michelle", "love", "sunshine",
    "jessica", "asshole", "696969", "amanda", "access", "computer", "cookie",
    "mickey", "secret", "maxwell", "mustang", "marcus", "jordan23", "super",
    "allison", "soccer1", "tiger", "badass", "chevy", "white", "black",
    "fishing", "blowme", "fishing1", "debbie", "miami", "squirt", "gators",
    "packers", "jordan1", "cowboys", "eagles", "chris", "liverpool", "gordon",
    "casper", "stupid", "shit", "saturn", "gemini", "apples", "august",
    "canada", "blazer", "cumming", "hunting", "kitty", "rainbow", "arthur",
    "cream", "calvin", "shaved", "surfer", "samson", "kelly1", "paul",
    "matt", "qwerty1", "john", "robert1", "daniel", "chris1", "george1",
    "david1", "thomas1", "steven", "brian", "kevin", "jason", "matthew",
    "gary", "timothy", "jose", "larry", "jeffrey", "frank", "scott", "eric",
    "stephen", "andrew1", "raymond", "gregory", "joshua", "jerry", "dennis",
    "walter", "peter", "harold", "douglas", "henry", "carl", "arthur1",
    "ryan", "roger", "joe", "juan", "jack", "albert", "jonathan", "justin",
    "terry", "gerald", "keith", "samuel", "willie", "ralph", "lawrence",
    "nicholas", "roy", "benjamin", "bruce", "brandon", "adam", "harry",
    "fred", "wayne", "billy", "steve", "louis", "jeremy", "aaron", "randy",
    "howard", "eugene", "carlos", "russell", "bobby", "victor", "martin",
    "ernest", "phillip", "todd", "jesse", "craig", "alan", "shawn", "clarence",
    "sean", "philip", "chris", "johnny", "earl", "jimmy", "antonio", "danny",
    "bryan", "tony", "luis", "mike", "stanley", "leonard", "nathan", "dale",
    "manuel", "rodney", "curtis", "norman", "allen", "marvin", "vincent",
    "glenn", "jeffery", "travis", "jeff", "chad", "jacob", "lee", "melvin",
    "alfred", "kyle", "francis", "bradley", "jesus", "herbert", "frederick",
    "ray", "joel", "edwin", "don", "eddie", "ricky", "troy", "randall",
    "barry", "alexander", "bernard", "mario", "leroy", "francisco", "marcus",
    "micheal", "theodore", "clifford", "miguel", "otis", "shane", "leslie",
    "omar", "angelo", "duane", "franklin", "andres", "elmer", "brad",
    "gabriel", "ron", "mitchell", "roland", "arnold", "harvey", "jared",
    "adrian", "karl", "cory", "claude", "erik", "darryl", "jamie", "neil",
    "jessie", "christian", "javier", "fernando", "clinton", "ted", "mathew",
    "tyrone", "darren", "lonnie", "lance", "cody", "julio", "kelly1",
    "kurt", "allan", "nelson", "guy", "clayton", "hugh", "max", "dwayne",
    "dwight", "armando", "felix", "jimmie", "everett", "jordan", "ian",
    "wallace", "ken", "bob", "jaime", "casey", "alfredo", "alberto",
    "dave", "ivan", "johnnie", "sidney", "byron", "julian", "isaac",
    "morris", "clifton", "willard", "daryl", "ross", "virgil", "dylan",
    "dewey", "al", "kristopher", "erika", "jaime", "casey", "alfredo",
    "alberto", "dave", "ivan", "johnnie", "sidney", "byron", "julian",
    "isaac", "morris", "clifton", "willard", "daryl", "ross", "virgil",
    "dylan", "dewey", "al", "kristopher", "erika", "jaime", "casey",
    "alfredo", "alberto", "dave", "ivan", "johnnie", "sidney", "byron",
    "julian", "isaac", "morris", "clifton", "willard", "daryl", "ross",
    "virgil", "dylan", "dewey", "al", "kristopher", "erika",
    
    # 中文常用密码
    "123456", "666666", "888888", "000000", "111111", "222222", "333333",
    "444444", "555555", "777777", "999999", "123123", "456456", "789789",
    "abc123", "abc456", "abc789", "qwe123", "qwe456", "qwe789",
    "asd123", "asd456", "asd789", "zxc123", "zxc456", "zxc789",
    "admin", "admin123", "admin456", "admin789", "root", "root123",
    "password", "password123", "password456", "password789",
    "123456789", "1234567890", "12345678901", "123456789012",
    "qwerty", "qwerty123", "qwerty456", "qwerty789",
    "asdfgh", "asdfgh123", "asdfgh456", "asdfgh789",
    "zxcvbn", "zxcvbn123", "zxcvbn456", "zxcvbn789",
    "1qaz2wsx", "2wsx3edc", "3edc4rfv", "4rfv5tgb", "5tgb6yhn",
    "6yhn7ujm", "7ujm8ik", "8ik9ol", "9ol0p",
    "qazwsx", "wsxedc", "edcrfv", "rfvtgb", "tgbyhn", "yhnujm",
    "ujmik", "ikol", "olp", "p;'",
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "qwertyuiop123", "asdfghjkl123", "zxcvbnm123",
    "qwertyuiop456", "asdfghjkl456", "zxcvbnm456",
    "qwertyuiop789", "asdfghjkl789", "zxcvbnm789",
    
    # 年份组合
    "2020", "2021", "2022", "2023", "2024", "2025",
    "2020!", "2021!", "2022!", "2023!", "2024!", "2025!",
    "2020@", "2021@", "2022@", "2023@", "2024@", "2025@",
    "2020#", "2021#", "2022#", "2023#", "2024#", "2025#",
    "2020$", "2021$", "2022$", "2023$", "2024$", "2025$",
    "2020%", "2021%", "2022%", "2023%", "2024%", "2025%",
    "2020^", "2021^", "2022^", "2023^", "2024^", "2025^",
    "2020&", "2021&", "2022&", "2023&", "2024&", "2025&",
    "2020*", "2021*", "2022*", "2023*", "2024*", "2025*",
    "2020(", "2021(", "2022(", "2023(", "2024(", "2025(",
    "2020)", "2021)", "2022)", "2023)", "2024)", "2025)",
    "2020-", "2021-", "2022-", "2023-", "2024-", "2025-",
    "2020_", "2021_", "2022_", "2023_", "2024_", "2025_",
    "2020+", "2021+", "2022+", "2023+", "2024+", "2025+",
    "2020=", "2021=", "2022=", "2023=", "2024=", "2025=",
    "2020[", "2021[", "2022[", "2023[", "2024[", "2025[",
    "2020]", "2021]", "2022]", "2023]", "2024]", "2025]",
    "2020{", "2021{", "2022{", "2023{", "2024{", "2025{",
    "2020}", "2021}", "2022}", "2023}", "2024}", "2025}",
    "2020|", "2021|", "2022|", "2023|", "2024|", "2025|",
    "2020\\", "2021\\", "2022\\", "2023\\", "2024\\", "2025\\",
    "2020:", "2021:", "2022:", "2023:", "2024:", "2025:",
    "2020;", "2021;", "2022;", "2023;", "2024;", "2025;",
    "2020\"", "2021\"", "2022\"", "2023\"", "2024\"", "2025\"",
    "2020'", "2021'", "2022'", "2023'", "2024'", "2025'",
    "2020<", "2021<", "2022<", "2023<", "2024<", "2025<",
    "2020>", "2021>", "2022>", "2023>", "2024>", "2025>",
    "2020,", "2021,", "2022,", "2023,", "2024,", "2025,",
    "2020.", "2021.", "2022.", "2023.", "2024.", "2025.",
    "2020?", "2021?", "2022?", "2023?", "2024?", "2025?",
    "2020/", "2021/", "2022/", "2023/", "2024/", "2025/",
    
    # 手机号前缀
    "138", "139", "150", "151", "152", "157", "158", "159",
    "186", "187", "188", "189", "130", "131", "132", "133",
    "134", "135", "136", "137", "180", "181", "182", "183",
    "184", "185", "170", "171", "172", "173", "175", "176",
    "177", "178", "147", "145", "146", "148", "149",
    
    # 生日组合
    "0101", "0201", "0301", "0401", "0501", "0601", "0701", "0801", "0901", "1001", "1101", "1201",
    "0102", "0202", "0302", "0402", "0502", "0602", "0702", "0802", "0902", "1002", "1102", "1202",
    "0103", "0203", "0303", "0403", "0503", "0603", "0703", "0803", "0903", "1003", "1103", "1203",
    "0104", "0204", "0304", "0404", "0504", "0604", "0704", "0804", "0904", "1004", "1104", "1204",
    "0105", "0205", "0305", "0405", "0505", "0605", "0705", "0805", "0905", "1005", "1105", "1205",
    "0106", "0206", "0306", "0406", "0506", "0606", "0706", "0806", "0906", "1006", "1106", "1206",
    "0107", "0207", "0307", "0407", "0507", "0607", "0707", "0807", "0907", "1007", "1107", "1207",
    "0108", "0208", "0308", "0408", "0508", "0608", "0708", "0808", "0908", "1008", "1108", "1208",
    "0109", "0209", "0309", "0409", "0509", "0609", "0709", "0809", "0909", "1009", "1109", "1209",
    "0110", "0210", "0310", "0410", "0510", "0610", "0710", "0810", "0910", "1010", "1110", "1210",
    "0111", "0211", "0311", "0411", "0511", "0611", "0711", "0811", "0911", "1011", "1111", "1211",
    "0112", "0212", "0312", "0412", "0512", "0612", "0712", "0812", "0912", "1012", "1112", "1212",
    "0113", "0213", "0313", "0413", "0513", "0613", "0713", "0813", "0913", "1013", "1113", "1213",
    "0114", "0214", "0314", "0414", "0514", "0614", "0714", "0814", "0914", "1014", "1114", "1214",
    "0115", "0215", "0315", "0415", "0515", "0615", "0715", "0815", "0915", "1015", "1115", "1215",
    "0116", "0216", "0316", "0416", "0516", "0616", "0716", "0816", "0916", "1016", "1116", "1216",
    "0117", "0217", "0317", "0417", "0517", "0617", "0717", "0817", "0917", "1017", "1117", "1217",
    "0118", "0218", "0318", "0418", "0518", "0618", "0718", "0818", "0918", "1018", "1118", "1218",
    "0119", "0219", "0319", "0419", "0519", "0619", "0719", "0819", "0919", "1019", "1119", "1219",
    "0120", "0220", "0320", "0420", "0520", "0620", "0720", "0820", "0920", "1020", "1120", "1220",
    "0121", "0221", "0321", "0421", "0521", "0621", "0721", "0821", "0921", "1021", "1121", "1221",
    "0122", "0222", "0322", "0422", "0522", "0622", "0722", "0822", "0922", "1022", "1122", "1222",
    "0123", "0223", "0323", "0423", "0523", "0623", "0723", "0823", "0923", "1023", "1123", "1223",
    "0124", "0224", "0324", "0424", "0524", "0624", "0724", "0824", "0924", "1024", "1124", "1224",
    "0125", "0225", "0325", "0425", "0525", "0625", "0725", "0825", "0925", "1025", "1125", "1225",
    "0126", "0226", "0326", "0426", "0526", "0626", "0726", "0826", "0926", "1026", "1126", "1226",
    "0127", "0227", "0327", "0427", "0527", "0627", "0727", "0827", "0927", "1027", "1127", "1227",
    "0128", "0228", "0328", "0428", "0528", "0628", "0728", "0828", "0928", "1028", "1128", "1228",
    "0129", "0229", "0329", "0429", "0529", "0629", "0729", "0829", "0929", "1029", "1129", "1229",
    "0130", "0230", "0330", "0430", "0530", "0630", "0730", "0830", "0930", "1030", "1130", "1230",
    "0131", "0231", "0331", "0431", "0531", "0631", "0731", "0831", "0931", "1031", "1131", "1231",
    
    # 特殊组合
    "admin123", "root123", "user123", "test123", "demo123",
    "password123", "pass123", "pwd123", "secret123", "key123",
    "admin@123", "root@123", "user@123", "test@123", "demo@123",
    "password@123", "pass@123", "pwd@123", "secret@123", "key@123",
    "admin#123", "root#123", "user#123", "test#123", "demo#123",
    "password#123", "pass#123", "pwd#123", "secret#123", "key#123",
    "admin$123", "root$123", "user$123", "test$123", "demo$123",
    "password$123", "pass$123", "pwd$123", "secret$123", "key$123",
    "admin%123", "root%123", "user%123", "test%123", "demo%123",
    "password%123", "pass%123", "pwd%123", "secret%123", "key%123",
    "admin^123", "root^123", "user^123", "test^123", "demo^123",
    "password^123", "pass^123", "pwd^123", "secret^123", "key^123",
    "admin&123", "root&123", "user&123", "test&123", "demo&123",
    "password&123", "pass&123", "pwd&123", "secret&123", "key&123",
    "admin*123", "root*123", "user*123", "test*123", "demo*123",
    "password*123", "pass*123", "pwd*123", "secret*123", "key*123",
    "admin(123", "root(123", "user(123", "test(123", "demo(123",
    "password(123", "pass(123", "pwd(123", "secret(123", "key(123",
    "admin)123", "root)123", "user)123", "test)123", "demo)123",
    "password)123", "pass)123", "pwd)123", "secret)123", "key)123",
    "admin-123", "root-123", "user-123", "test-123", "demo-123",
    "password-123", "pass-123", "pwd-123", "secret-123", "key-123",
    "admin_123", "root_123", "user_123", "test_123", "demo_123",
    "password_123", "pass_123", "pwd_123", "secret_123", "key_123",
    "admin+123", "root+123", "user+123", "test+123", "demo+123",
    "password+123", "pass+123", "pwd+123", "secret+123", "key+123",
    "admin=123", "root=123", "user=123", "test=123", "demo=123",
    "password=123", "pass=123", "pwd=123", "secret=123", "key=123",
    "admin[123", "root[123", "user[123", "test[123", "demo[123",
    "password[123", "pass[123", "pwd[123", "secret[123", "key[123",
    "admin]123", "root]123", "user]123", "test]123", "demo]123",
    "password]123", "pass]123", "pwd]123", "secret]123", "key]123",
    "admin{123", "root{123", "user{123", "test{123", "demo{123",
    "password{123", "pass{123", "pwd{123", "secret{123", "key{123",
    "admin}123", "root}123", "user}123", "test}123", "demo}123",
    "password}123", "pass}123", "pwd}123", "secret}123", "key}123",
    "admin|123", "root|123", "user|123", "test|123", "demo|123",
    "password|123", "pass|123", "pwd|123", "secret|123", "key|123",
    "admin\\123", "root\\123", "user\\123", "test\\123", "demo\\123",
    "password\\123", "pass\\123", "pwd\\123", "secret\\123", "key\\123",
    "admin:123", "root:123", "user:123", "test:123", "demo:123",
    "password:123", "pass:123", "pwd:123", "secret:123", "key:123",
    "admin;123", "root;123", "user;123", "test;123", "demo;123",
    "password;123", "pass;123", "pwd;123", "secret;123", "key;123",
    "admin\"123", "root\"123", "user\"123", "test\"123", "demo\"123",
    "password\"123", "pass\"123", "pwd\"123", "secret\"123", "key\"123",
    "admin'123", "root'123", "user'123", "test'123", "demo'123",
    "password'123", "pass'123", "pwd'123", "secret'123", "key'123",
    "admin<123", "root<123", "user<123", "test<123", "demo<123",
    "password<123", "pass<123", "pwd<123", "secret<123", "key<123",
    "admin>123", "root>123", "user>123", "test>123", "demo>123",
    "password>123", "pass>123", "pwd>123", "secret>123", "key>123",
    "admin,123", "root,123", "user,123", "test,123", "demo,123",
    "password,123", "pass,123", "pwd,123", "secret,123", "key,123",
    "admin.123", "root.123", "user.123", "test.123", "demo.123",
    "password.123", "pass.123", "pwd.123", "secret.123", "key.123",
    "admin?123", "root?123", "user?123", "test?123", "demo?123",
    "password?123", "pass?123", "pwd?123", "secret?123", "key?123",
    "admin/123", "root/123", "user/123", "test/123", "demo/123",
    "password/123", "pass/123", "pwd/123", "secret/123", "key/123",
    
    # 键盘模式
    "qwerty", "asdfgh", "zxcvbn", "123456", "654321",
    "qazwsx", "edcrfv", "tgbyhn", "ujmikl", "plokij",
    "mnbvcx", "lkjhgf", "dsapoi", "rewq", "fdsa",
    "vcxz", "bgt", "nhy", "mju", "kil",
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "qwertyuiop123", "asdfghjkl123", "zxcvbnm123",
    "qwertyuiop456", "asdfghjkl456", "zxcvbnm456",
    "qwertyuiop789", "asdfghjkl789", "zxcvbnm789",
    "qwertyuiop!@#", "asdfghjkl!@#", "zxcvbnm!@#",
    "qwertyuiop$%^", "asdfghjkl$%^", "zxcvbnm$%^",
    "qwertyuiop&*(", "asdfghjkl&*(", "zxcvbnm&*(",
    "qwertyuiop)_+", "asdfghjkl)_+", "zxcvbnm)_+",
    "qwertyuiop-=", "asdfghjkl-=", "zxcvbnm-=",
    "qwertyuiop[]", "asdfghjkl[]", "zxcvbnm[]",
    "qwertyuiop{}", "asdfghjkl{}", "zxcvbnm{}",
    "qwertyuiop|\\", "asdfghjkl|\\", "zxcvbnm|\\",
    "qwertyuiop:;", "asdfghjkl:;", "zxcvbnm:;",
    "qwertyuiop\"'", "asdfghjkl\"'", "zxcvbnm\"'",
    "qwertyuiop<>", "asdfghjkl<>", "zxcvbnm<>",
    "qwertyuiop,.", "asdfghjkl,.", "zxcvbnm,.",
    "qwertyuiop/?", "asdfghjkl/?", "zxcvbnm/?",
    
    # 重复模式
    "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa", "aaaaaaaa",
    "bb", "bbb", "bbbb", "bbbbb", "bbbbbb", "bbbbbbb", "bbbbbbbb",
    "cc", "ccc", "cccc", "ccccc", "cccccc", "ccccccc", "cccccccc",
    "dd", "ddd", "dddd", "ddddd", "dddddd", "ddddddd", "dddddddd",
    "ee", "eee", "eeee", "eeeee", "eeeeee", "eeeeeee", "eeeeeeee",
    "ff", "fff", "ffff", "fffff", "ffffff", "fffffff", "ffffffff",
    "gg", "ggg", "gggg", "ggggg", "gggggg", "ggggggg", "gggggggg",
    "hh", "hhh", "hhhh", "hhhhh", "hhhhhh", "hhhhhhh", "hhhhhhhh",
    "ii", "iii", "iiii", "iiiii", "iiiiii", "iiiiiii", "iiiiiiii",
    "jj", "jjj", "jjjj", "jjjjj", "jjjjjj", "jjjjjjj", "jjjjjjjj",
    "kk", "kkk", "kkkk", "kkkkk", "kkkkkk", "kkkkkkk", "kkkkkkkk",
    "ll", "lll", "llll", "lllll", "llllll", "lllllll", "llllllll",
    "mm", "mmm", "mmmm", "mmmmm", "mmmmmm", "mmmmmmm", "mmmmmmmm",
    "nn", "nnn", "nnnn", "nnnnn", "nnnnnn", "nnnnnnn", "nnnnnnnn",
    "oo", "ooo", "oooo", "ooooo", "oooooo", "ooooooo", "oooooooo",
    "pp", "ppp", "pppp", "ppppp", "pppppp", "ppppppp", "pppppppp",
    "qq", "qqq", "qqqq", "qqqqq", "qqqqqq", "qqqqqqq", "qqqqqqqq",
    "rr", "rrr", "rrrr", "rrrrr", "rrrrrr", "rrrrrrr", "rrrrrrrr",
    "ss", "sss", "ssss", "sssss", "ssssss", "sssssss", "ssssssss",
    "tt", "ttt", "tttt", "ttttt", "tttttt", "ttttttt", "tttttttt",
    "uu", "uuu", "uuuu", "uuuuu", "uuuuuu", "uuuuuuu", "uuuuuuuu",
    "vv", "vvv", "vvvv", "vvvvv", "vvvvvv", "vvvvvvv", "vvvvvvvv",
    "ww", "www", "wwww", "wwwww", "wwwwww", "wwwwwww", "wwwwwwww",
    "xx", "xxx", "xxxx", "xxxxx", "xxxxxx", "xxxxxxx", "xxxxxxxx",
    "yy", "yyy", "yyyy", "yyyyy", "yyyyyy", "yyyyyyy", "yyyyyyyy",
    "zz", "zzz", "zzzz", "zzzzz", "zzzzzz", "zzzzzzz", "zzzzzzzz",
    
    # 数字重复
    "00", "000", "0000", "00000", "000000", "0000000", "00000000",
    "11", "111", "1111", "11111", "111111", "1111111", "11111111",
    "22", "222", "2222", "22222", "222222", "2222222", "22222222",
    "33", "333", "3333", "33333", "333333", "3333333", "33333333",
    "44", "444", "4444", "44444", "444444", "4444444", "44444444",
    "55", "555", "5555", "55555", "555555", "5555555", "55555555",
    "66", "666", "6666", "66666", "666666", "6666666", "66666666",
    "77", "777", "7777", "77777", "777777", "7777777", "77777777",
    "88", "888", "8888", "88888", "888888", "8888888", "88888888",
    "99", "999", "9999", "99999", "999999", "9999999", "99999999",
    
    # 特殊字符重复
    "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", "!!!!!!!", "!!!!!!!!",
    "@@", "@@@", "@@@@", "@@@@@", "@@@@@@", "@@@@@@@", "@@@@@@@@",
    "##", "###", "####", "#####", "######", "#######", "########",
    "$$", "$$$", "$$$$", "$$$$$", "$$$$$$", "$$$$$$$", "$$$$$$$$",
    "%%", "%%%", "%%%%", "%%%%%", "%%%%%%", "%%%%%%%", "%%%%%%%%",
    "^^", "^^^", "^^^^", "^^^^^", "^^^^^^", "^^^^^^^", "^^^^^^^^",
    "&&", "&&&", "&&&&", "&&&&&", "&&&&&&", "&&&&&&&", "&&&&&&&&",
    "**", "***", "****", "*****", "******", "*******", "********",
    "((", "(((", "((((", "(((((", "(((((((", "((((((((", "(((((((((",
    "))", ")))", "))))", ")))))", "))))))", ")))))))", "))))))))",
    "--", "---", "----", "-----", "------", "-------", "--------",
    "__", "___", "____", "_____", "______", "_______", "________",
    "++", "+++", "++++", "+++++", "++++++", "+++++++", "++++++++",
    "==", "===", "====", "=====", "======", "=======", "========",
    "[[", "[[[", "[[[[", "[[[[[", "[[[[[[", "[[[[[[[", "[[[[[[[[",
    "]]", "]]]", "]]]]", "]]]]]", "]]]]]]", "]]]]]]]", "]]]]]]]]",
    "{{", "{{{", "{{{{", "{{{{{", "{{{{{{", "{{{{{{{", "{{{{{{{{",
    "}}", "}}}", "}}}}", "}}}}}", "}}}}}}", "}}}}}}}", "}}}}}}}}",
    "||", "|||", "||||", "|||||", "||||||", "|||||||", "||||||||",
    "\\\\", "\\\\\\", "\\\\\\\\", "\\\\\\\\\\", "\\\\\\\\\\\\", "\\\\\\\\\\\\\\", "\\\\\\\\\\\\\\\\",
    "::", ":::", "::::", ":::::", "::::::", ":::::::", "::::::::",
    ";;", ";;;", ";;;;", ";;;;;", ";;;;;;", ";;;;;;;", ";;;;;;;;",
    "\"\"", "\"\"\"", "\"\"\"\"", "\"\"\"\"\"", "\"\"\"\"\"\"", "\"\"\"\"\"\"\"", "\"\"\"\"\"\"\"\"",
    "''", "'''", "''''", "'''''", "''''''", "'''''''", "''''''''",
    "<<", "<<<", "<<<<", "<<<<<", "<<<<<<", "<<<<<<<", "<<<<<<<<",
    ">>", ">>>", ">>>>", ">>>>>", ">>>>>>", ">>>>>>>", ">>>>>>>>",
    ",,", ",,,", ",,,,", ",,,,,", ",,,,,,", ",,,,,,,", ",,,,,,,,",
    "..", "...", "....", ".....", "......", ".......", "........",
    "??", "???", "????", "?????", "??????", "???????", "????????",
    "//", "///", "////", "/////", "//////", "///////", "////////",
]

# 年份和日期组合（示例，实际可以动态生成）
YEARS = [str(y) for y in range(1990, 2026)]
COMMON_DATES = ["0101", "1231", "0808"]

# 常见字符替换规则
REPLACEMENT_RULES = {
    'a': ['@', '4'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['$', '5'],
    't': ['7'],
    'l': ['1'],
    'A': ['@', '4'],
    'E': ['3'],
    'I': ['1', '!'],
    'O': ['0'],
    'S': ['$', '5'],
    'T': ['7'],
    'L': ['1'],
}

def generate_rule_passwords(base_words):
    """
    根据规则生成密码。
    简单示例：添加年份，首字母大写等。
    """
    generated_passwords = set(base_words)

    for word in base_words:
        # 添加年份
        for year in YEARS:
            generated_passwords.add(word + year)
            generated_passwords.add(year + word)
        # 添加常见日期
        for date in COMMON_DATES:
            generated_passwords.add(word + date)
            generated_passwords.add(date + word)

        # 首字母大写
        if len(word) > 0:
            generated_passwords.add(word[0].upper() + word[1:])

        # 尾部添加特殊字符
        for char in "!@#$%^":
            generated_passwords.add(word + char)
            generated_passwords.add(char + word)

        # 简单替换
        temp_word = list(word)
        for i, char in enumerate(temp_word):
            if char in REPLACEMENT_RULES:
                for replacement in REPLACEMENT_RULES[char]:
                    original_char = temp_word[i]
                    temp_word[i] = replacement
                    generated_passwords.add("".join(temp_word))
                    temp_word[i] = original_char # 恢复，进行下一个替换

    return sorted(list(generated_passwords))

def generate_mask_passwords(mask):
    """
    根据掩码生成密码。
    掩码示例: ?l?l?d?d?d
    ?l: 小写字母
    ?u: 大写字母
    ?d: 数字
    ?s: 特殊字符
    ?a: 所有字符 (小写、大写、数字、特殊)
    """
    charsets = {
        '?l': string.ascii_lowercase,
        '?u': string.ascii_uppercase,
        '?d': string.digits,
        '?s': string.punctuation,
        '?a': string.ascii_letters + string.digits + string.punctuation
    }

    # 解析掩码，将掩码中的特殊序列替换为对应的字符集
    parsed_mask_components = []
    i = 0
    while i < len(mask):
        if mask[i] == '?' and i + 1 < len(mask):
            char_code = mask[i:i+2]
            if char_code in charsets:
                parsed_mask_components.append(charsets[char_code])
                i += 2
            else:
                # 如果是未知掩码字符，按原样处理
                parsed_mask_components.append(mask[i])
                i += 1
        else:
            parsed_mask_components.append(mask[i])
            i += 1

    # 生成所有可能的组合
    for combination in itertools.product(*parsed_mask_components):
        yield "".join(combination)

def verify_zip_password(file_path, password):
    """
    验证ZIP文件密码的有效性。
    尝试用密码打开并解压文件，如果成功则密码正确。
    """
    temp_dir = None
    try:
        # 尝试用密码打开ZIP文件
        with zipfile.ZipFile(file_path, 'r') as zf:
            # 创建临时目录
            temp_dir = f"temp_extract_{os.path.basename(file_path)}_{time.time()}"
            os.makedirs(temp_dir, exist_ok=True)
            
            # 尝试解压文件到临时目录以验证密码
            zf.extractall(path=temp_dir, pwd=password.encode())
            return True
    except RuntimeError as e:
        # 通常是密码错误导致 RuntimeError: Bad password for file
        if "Bad password for file" in str(e) or "password required" in str(e).lower():
            return False
        return False
    except zipfile.BadZipFile:
        # 文件损坏或不是有效的zip文件格式
        return False
    except Exception as e:
        # 捕获其他所有未知异常
        return False
    finally:
        # 无论成功、失败或异常，都尝试清理临时目录
        if temp_dir and os.path.exists(temp_dir):
            try:
                for root, dirs, files in os.walk(temp_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(temp_dir)
            except Exception as e:
                # print(f"清理临时目录失败: {e}") # 可以添加更详细的日志，但避免在UI中过度显示
                pass # 忽略清理失败的错误

def crack(file_path, mode, log_callback, progress_callback, min_length=1, max_length=8, charset="all", mask=None, wordlist=None, progress_data=None, stop_event=None, pause_event=None, **kwargs):
    log_callback(f"开始破解ZIP文件: {file_path}, 模式: {mode}")
    import string
    charset_dict = {
        "数字": string.digits,
        "小写字母": string.ascii_lowercase,
        "大写字母": string.ascii_uppercase,
        "字母": string.ascii_letters,
        "符号": string.punctuation,
        "全字符集": string.ascii_letters + string.digits + string.punctuation,
        "all": string.ascii_letters + string.digits + string.punctuation
    }
    charset_str = charset_dict.get(charset, string.ascii_lowercase)
    if mode == "brute":
        total = sum(len(charset_str) ** l for l in range(min_length, max_length + 1))
        attempt = 0
        for length in range(min_length, max_length + 1):
            for pwd_tuple in itertools.product(charset_str, repeat=length):
                if stop_event and stop_event.is_set():
                    log_callback("收到停止信号，破解中止。")
                    return {'success': False, 'message': '破解已停止'}
                while pause_event and pause_event.is_set():
                    time.sleep(0.1)
                password = ''.join(pwd_tuple)
                attempt += 1
                if attempt % 100 == 0 or attempt == total:
                    progress_callback(attempt, total, f"尝试: {password} [{attempt}/{total}]")
                try:
                    if verify_zip_password(file_path, password):
                        log_callback(f"[暴力破解] 破解成功！密码: {password}")
                        progress_callback(attempt, total, f"已破解，密码: {password}")
                        return {'success': True, 'password': password}
                except Exception as e:
                    log_callback(f"[错误] 尝试密码时异常: {e}")
        log_callback("[暴力破解] 未找到密码。")
        return {'success': False, 'message': '未找到密码'}
    elif mode == "mask":
        if not mask:
            log_callback("错误: 掩码模式需要提供掩码字符串。")
            return {'success': False, 'message': '掩码未提供'}
        
        # 使用高级掩码引擎
        try:
            from .advanced_mask_engine import crack_with_advanced_mask
            log_callback("使用高级掩码破解引擎...")
            
            result = crack_with_advanced_mask(
                file_path, mask, log_callback, progress_callback,
                stop_event, pause_event
            )
            
            if result:
                log_callback(f"[高级掩码破解] 破解成功！密码: {result}")
                return {'success': True, 'password': result}
            else:
                log_callback("[高级掩码破解] 未找到密码。")
                return {'success': False, 'message': '未找到密码'}
                
        except ImportError:
            # 如果高级引擎不可用，使用传统方法
            log_callback("高级引擎不可用，使用传统掩码破解...")
            def parse_mask(mask):
                mask_chars = {
                    '?l': string.ascii_lowercase,
                    '?u': string.ascii_uppercase,
                    '?d': string.digits,
                    '?s': string.punctuation,
                    '?a': string.ascii_letters + string.digits + string.punctuation
                }
                charset_list = []
                i = 0
                while i < len(mask):
                    if mask[i:i+2] in mask_chars:
                        charset_list.append(mask_chars[mask[i:i+2]])
                        i += 2
                    else:
                        charset_list.append(mask[i])
                        i += 1
                return charset_list
            
            charset_list = parse_mask(mask)
            total = 1
            for c in charset_list:
                total *= len(c)
            attempt = 0
            for pwd_tuple in itertools.product(*charset_list):
                if stop_event and stop_event.is_set():
                    log_callback("收到停止信号，破解中止。")
                    return {'success': False, 'message': '破解已停止'}
                while pause_event and pause_event.is_set():
                    time.sleep(0.1)
                password = ''.join(pwd_tuple)
                attempt += 1
                if attempt % 100 == 0 or attempt == total:
                    progress_callback(attempt, total, f"掩码: {password} [{attempt}/{total}]")
                try:
                    if verify_zip_password(file_path, password):
                        log_callback(f"[掩码破解] 破解成功！密码: {password}")
                        progress_callback(attempt, total, f"已破解，密码: {password}")
                        return {'success': True, 'password': password}
                except Exception as e:
                    log_callback(f"[错误] 尝试密码时异常: {e}")
            log_callback("[掩码破解] 未找到密码。")
            return {'success': False, 'message': '未找到密码'}
    elif mode == "dict" or mode == "auto":
        passwords = set(ENHANCED_DICTIONARY)
        if wordlist and os.path.exists(wordlist):
            try:
                with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords.update([line.strip() for line in f if line.strip()])
            except Exception as e:
                log_callback(f"加载外部字典失败: {e}")
        passwords = sorted(list(passwords))
        total_passwords = len(passwords)
        attempt_count = 0
        for password in passwords:
            if stop_event and stop_event.is_set():
                log_callback("ZIP破解已停止。")
                return {'success': False, 'message': '破解已停止'}
            if pause_event and pause_event.is_set():
                while pause_event.is_set():
                    time.sleep(0.1)
                    if stop_event and stop_event.is_set():
                        log_callback("ZIP破解已停止。")
                        return {'success': False, 'message': '破解已停止'}
            attempt_count += 1
            progress_callback(attempt_count, total_passwords, f"尝试密码: {password} (已尝试: {attempt_count})")
            if verify_zip_password(file_path, password):
                log_callback(f"ZIP文件破解成功！密码: {password}")
                return {'success': True, 'password': password}
        log_callback("ZIP文件破解失败，未找到密码。")
        return {'success': False, 'message': '未找到密码'}
    elif mode == "ai":
        log_callback("AI 预测模式正在初始化...")
        passwords = ["AI_predicted_password_123", "AI_guess_strong"]
        total_passwords = len(passwords)
        password_iterator = iter(passwords)
        
    elif mode == "hashcat":
        log_callback("调用 Hashcat 引擎进行破解...")
        return {'success': False, 'message': 'Hashcat 引擎未集成'}
    elif mode == "john":
        log_callback("调用 John the Ripper 引擎进行破解...")
        return {'success': False, 'message': 'John the Ripper 引擎未集成'}
    else:
        log_callback(f"未知或不支持的破解模式: {mode}")
        return {'success': False, 'message': '未知模式'}

    attempt_count = 0
    if password_iterator is None:
        return {'success': False, 'message': '密码迭代器未初始化'}

    for password in password_iterator:
        if isinstance(password, tuple):
            password = "".join(password)

        # 检查停止事件
        if stop_event and stop_event.is_set():
            log_callback("ZIP破解已停止。")
            return {'success': False, 'message': '破解已停止'}
        
        # 检查暂停事件
        if pause_event and pause_event.is_set():
            while pause_event.is_set():
                time.sleep(0.1)
                if stop_event and stop_event.is_set():
                    log_callback("ZIP破解已停止。")
                    return {'success': False, 'message': '破解已停止'}

        attempt_count += 1
        progress_callback(attempt_count, total_passwords, f"尝试密码: {password} (已尝试: {attempt_count})")
        
        if verify_zip_password(file_path, password):
            log_callback(f"ZIP文件破解成功！密码: {password}")
            return {'success': True, 'password': password}
        
    log_callback("ZIP文件破解失败，未找到密码。")
    return {'success': False, 'message': '未找到密码'}

def crack_zip_bruteforce(file_path, update_progress_callback, stop_event, pause_event, log_callback, min_length=1, max_length=8, charset_name="all"):
    import string, time
    from itertools import product

    # 1. 优先尝试高概率密码
    common_passwords = ["123456", "password", "admin", "qwerty", "abc123", "111111"]
    for pwd in common_passwords:
        if stop_event.is_set():
            log_callback("收到停止信号，破解中止。")
            return None
        try:
            if verify_zip_password(file_path, pwd):
                log_callback(f"优先破解成功，密码：{pwd}")
                update_progress_callback(1, 1, f"已破解，密码：{pwd}")
                return pwd
        except Exception as e:
            log_callback(f"[错误] 优先密码尝试异常: {e}")

    # 2. 字符集
    charset_dict = {
        "numeric": string.digits,
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "mixed": string.ascii_letters,
        "all": string.ascii_letters + string.digits + string.punctuation,
        "数字": string.digits,
        "小写字母": string.ascii_lowercase,
        "大写字母": string.ascii_uppercase,
        "字母": string.ascii_letters,
        "符号": string.punctuation,
    }
    charset = charset_dict.get(charset_name, string.digits)
    total = sum(len(charset) ** l for l in range(min_length, max_length + 1))
    attempt = 0
    start_time = time.time()

    # 3. 动态生成密码，不卡内存
    for length in range(min_length, max_length + 1):
        for pwd_tuple in product(charset, repeat=length):
            if stop_event.is_set():
                log_callback("收到停止信号，破解中止。")
                return None
            while pause_event.is_set():
                time.sleep(0.1)
            password = ''.join(pwd_tuple)
            attempt += 1
            # 4. 进度刷新与CPU让步
            if attempt % 100 == 0 or attempt == total:
                elapsed = time.time() - start_time
                speed = attempt / elapsed if elapsed > 0 else 0
                remain = total - attempt
                eta = remain / speed if speed > 0 else -1
                eta_str = f"{int(eta)}s" if eta >= 0 else "--"
                percent = attempt * 100 // total if total > 0 else 0
                update_progress_callback(attempt, total, f"尝试: {password} [{attempt}/{total}] 进度: {percent}% 速度: {speed:.1f}/s 剩余: {remain} 预计: {eta_str}")
                log_callback(f"[暴力破解] 已尝试{attempt}个密码")
            if attempt % 500 == 0:
                time.sleep(0.001)
            # 5. 稳定性：异常捕获
            try:
                if verify_zip_password(file_path, password):
                    log_callback(f"[暴力破解] 破解成功！密码: {password}")
                    update_progress_callback(attempt, total, f"已破解，密码: {password}")
                    stop_event.set()
                    return password
            except Exception as e:
                log_callback(f"[错误] 尝试密码时异常: {e}")
    log_callback("[暴力破解] 未找到密码。")
    return None 