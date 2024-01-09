from trrne.lottery import LotteryPair

test = 'test!'

channel_ids: dict[str, int] = {
    'x128_ch': 854616415323815936,
    'x128_vc': 854629372497756160,
    'x128_log': 1007274150072697003,
    'hon': 738673709803503678,
    'tamani_ch': 854616415323815939,
    'moonie_ch': 854616439544610827,
    'test': 1007270260912685126,
    'test_ch': 913030261501984768,
    'test_2': 732942987331633202,
    'test_vc': 882616446302187580,
}

user_ids: dict[str, int] = {
    'honmany': 738673709803503678,
    'leo': 854655602503974923,
    'maru': 641902369407500288,
    'katsu': 640880132101373964,
    'niko': 657910904288968705,
    'yuto': 329959570980077569,
    'hanako': 672376985821118484,
    'fuku': 728582984684535909,
    'ren': 603495382051323905,
    'tomo': 665470238636376076,
    'seto': 283584931437871104,
}

jokes = [
    '布団が吹っ飛んだ',
    '傷んだ廊下に居たんだろうか',
    '都心に突進',
    'レモンのいれもん',
    'ジャムおじさんがジャムを持参',
    'トイレにいっといれ',
    '蛙が帰る',
    '内臓がないぞー',
    'タモリがいた森',
    '社畜のシャチ君',
    'アルミ缶の上にあるみかん',
]

lol = [
    'もっと笑えよ',
    '真顔で笑うな',
    '( ´∀｀ )',
]


warikitte = [
    '無理っす',  # 0
    '無理っす絶対無理っす',
    '割り切って',
    'そこをなんとか割り切ってほしいんだよね',
]

ofurosuki = [
    '呼んだ？',
    '呼んだよね？'
]

vids = [
    'https://youtu.be/OCf5KMXF3mQ',  # warikiri
    'https://youtu.be/2sKgVz79NZE',  # houki
    'https://youtu.be/n2FW6UUCRq4',  # docho
    'https://youtu.be/w_gLXxBQ9ro',  # tame
    'https://youtu.be/NzxfV-SuVeU',  # morai
    'https://youtu.be/KNuzE4nq8H4',  # tinpira
    'https://youtu.be/rgPb92A7IzA',  # gohome
    'https://youtu.be/R--vio7AAv8',  # enter
    'https://youtu.be/JIWnVhb8Wwk',  # muti
    'https://youtu.be/B5SuJuCivgo',  # kutibiru
    'https://youtu.be/8IbPNS7YYCI',  # keno
    'https://youtu.be/X_XvoB0sE7A',  # boukyaku
    'https://youtu.be/Bo2AfLyaM6w',  # omae
    'https://youtu.be/DX9MYITMc9Q',  # kyodori
    'https://youtu.be/FHOACaOJunM',  # bibiri
    'https://youtu.be/LIST6Vgn9M0',  # keni
    'https://youtu.be/O1URzreoDhQ',  # hondai
    'https://youtu.be/VN0uyzD57jE',  # shusse
    'https://youtu.be/ikeVY6i9Rdk',  # yume
    'https://youtu.be/Ur3hWO9mMPg',  # rookie
    'https://youtu.be/MIf24vGAMxY',  # sentakusi
    'https://youtu.be/4ya03BdxDmE',  # nakazawa
]

kuji = LotteryPair([
    ('ほんまに大吉', 0.5),
    ('たぶん中吉', 1.4),
    ('マジ吉', 1.2),
    ('しらんけど小吉', 1.0),
    ('どうせ凶', 0.7),
    ('おまえは大凶', 0.5),
    ('帝凶平成大学のここがすごい！', 0.01)
])
kuji_max_length = len('帝凶平成大学のここがすごい！')
