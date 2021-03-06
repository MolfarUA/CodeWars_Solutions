def _test_suite():
    times = [0, 0]
    
    def describe(*args):
        def d(times, *args):
            test.describe(*args)
            times[0] = timer()
        d(times, *args)
    
    def it(*args):
        def i(times, *args):
            test.it(*args)
            times[1] = timer()
        i(times, *args)
    
    def it_end():
        print('<COMPLETEDIN::> {:.2f}'.format((timer() - times[1]) * 1000))
    
    def describe_end():
        print('<COMPLETEDIN::> {:.2f}'.format((timer() - times[0]) * 1000))
        
    def test_one(s, title):
        it(title)
        solution = build_solution(get_data(s), 15)
        clues = build_clues(solution, 15)
        custom_assert_equals(clues, solution)
        it_end()
    
    describe('15x15 Nonograms Sample Tests')
    times[0] = time_start
    
    sample_inputs = [
        ('14724OOO346O7OOO7O6446O63449843448444834344836383434463838343448483834344N3434O5344O664N67-0O:0O;',
         'Sample Test: Book (Normal)'),
        ('147O484O3O3444486634383836344434484636343O363O4O444O358735440634687439743468743466683848358O3-0O:0O;',
         'Sample Test: Water Pot and Cup (Hard)'),
        ('188O4738363836384836483446383464374O848636442488458O324O3838363O386636384848483438343434346434384834348464843-0O:0O;',
         'Sample Test: Puppy (Hard)')
    ]
    for s, t in sample_inputs:
        test_one(s, t)
    
    describe_end()
    
    describe('15x15 Nonograms Random Tests')
    inputs = [
        '384774493440760869343486343764883434O8O43858482438O4346434346O3834O58484878O48396-0O:0O;',
        '38884O443634384844844466343434343848O43434463634344644343436446668384834444444443834343O8836443448383884366O3844344468864564-0O:0O;',
        '16784O3838443444344888343486343444354446374647674648473844444864364434488584448O84483448443O4868484C68-0O:0O;',
        '167N3O6O8O384844484634466444693448496842468N644N4645884424808434088044-0O:0O;',
        '17ON5926444484447636O444444444444444444477O4884686364O3O44383848443846348847483438464686OO3-0O:0O;',
        '1O704OOC946O54643465684864OOO844484884O468488884343437388434488438343848843434484838343845-0O:0O;',
        '1934803844086C483C36644748463O643438362834275437544O9437544747495O-0O:0O;',
        '1786873634363O34343434343O363436866884358884358864O484484644O447783648663834388444383668344456N73-0O:0O;',
        '1N6N4O47853O484O364734464744364748363O8846494684O43O44486O68443468374438483837343238443-0O:0O;',
        '3838478484388884443436344844343434349438483684673884493544642888844448843448648838844848378O445440444-0O:0O;',
        '146C3434454456443884883834374634358847ON6C80485O46O54N8845740640444-0O:0O;',
        '177299954848474438344784448666344658O43866O8674438854844474486443446343634343O884434463-0O:0O;',
        '1N4445483637863836384848388849O48544788O2438N7344666383OO737383O35383C38309-0O:0O;',
        '184687443867383634353434663848NO648448488O3844O4O45496884784O48444448444863736844744448984-0O:0O;',
        '1NON443404343434423430343434324434443437O4O788O84486844434343O3838348O363434343O38468O853996-0O:0O;',
        '183448893767873O84486844443444843734346437347446846434O94808O9O8868844O4O48486644839443-0O:0O;',
        '1580443404O506803846O6844944340684444764363768383634644836346238O8O8596-0O:0O;',
        '17444N525NO6458844344O3638443847344845484935465O444786N437295C8O-0O:0O;',
        '12O74634864436444638363466343644884734623434893434OO4434784834580O32363484446448444464806-0O:0O;',
        '1C34443485344444463408688O383484883O44O83O963O9646O83O48483444353444443486343438346O483655386-0O:0O;',
        '173084342484346444388448344444443444783834243408803838N63427348887343834873434448648443467484-0O:0O;',
        '15724O45454736464O3O3O3O3834883O3836383644344O3844343744643O8474O6347648446O34O445343465443-0O:0O;',
        '176867386837364635468238343N343446O4383438343434443838443498373234483588383O4448383O3848383734648O48-0O:0O;',
        '1O59393534444435343634353838343534483436695454848988342438303444043834243889863N38-0O:0O;',
        '1O404438686434383834683434344448843444344444343438O84438963754743888884434843434443434483434843844383634348638887636O-0O:0O;',
        '10386876666676466845483468484444486444383N348O6686346O48446438743834243834246424646-0O:0O;',
        '1O4687443634863838464634348948383C44824634393644354O34473O483O4738443434448634O44474O44466O44448-0O:0O;',
        '386854384438O4343444344834343438343434343434O446843434343438483O34464O34848648368668O43476687444483466644544O474O-0O:0O;',
        '3O7O38386848383884383448384438348838384O4836363438388864344434346834388858363668383848483844383438388438363868457O3-0O:0O;',
        '16724865483O3O483848363834383434383836343448383O3488383634383838443434884844384O48754636477834493O3437O4443-0O:0O;',
        '184947873446348O34363684443637463834378636373O363O34385836346448363464445444486448866446374440364-0O:0O;',
        '166C78378844343O4834383788448O3468343O3434574547387746463434474434344938343424O8343436343438O6O-0O:0O;',
        '1O6C468N9547883OO53836O83438886444368O843438668434488734348447344489444449444034447-0O:0O;',
        '1240443804443038340434343C483234446O3634484734343O7434378438443434444834446O863C44343C85-0O:0O;',
        '14308704344938684734884446443434343488343488384434383534363N4634343436374884453O89353935354746-0O:0O;',
        '148984443934883938O96N494O85478O48O446O8454O494O34356844353438343436843844343836443434343-0O:0O;',
        '1058OOO64804403538682484388O3438346O387478O6O84634463838384836388O848838483866664-0O:0O;',
        '193248624434325976O686644636484478344484383436348834344O34383438473834368836344O383638O63O35843-0O:0O;',
        '1N654636377635383649368748444534O43437353837O434493634396434354O3448643638344O4484343884848-0O:0O;',
        '19844N3444423838398N6O343886478544843O346O44344868O4323434698667604O64957-0O:0O;',
        '1234384234444238383N463259O5347O54893O444N6485444C363C3665454O893-0O:0O;',
        '184O883O48488434344434864634343O344664684436893484358484888434843444388O383644O6444444323838494436693C-0O:0O;',
        '1746493438383538883437373439343834393438344734363837464866O4344846366O383O888834383488343438443644787N-0O:0O;',
        '188588483O3834443448443448443834444434343834383448344434343O4O443735393438343784383480943838383464384834O848487838388-0O:0O;',
        '1842463445343434343O4438443O344436844434484884344834343834843834444834344444O4346O34364934303838N484N484N484O-0O:0O;',
        '1779744O7444364O443436384834343634383434344834643444483O383434483834344434383438444448343O344O383644463435344844374436424-0O:0O;',
        '168480346434743884743534OO56086N443438864464O88634343434343438546637343434383434347637373834343434383-0O:0O;',
        '164O6O68788448383O38363836346464348686O73785343O4464343834343O443834343O343444383648383OO838374O383O6874-0O:0O;',
        '14803844NO7686O4484874843438O84434446448364634O4364N36849O843634383888383848843434346488383888864-0O:0O;',
        '19843439408406408409773O38353O3836543838454448368434383434463434443438744434383738364948-0O:0O;',
        '183064O494665466768654O48646373644303988823O328037N838N48496864-0O:0O;',
        '10048037N79NO4868484348484344438O8344438O83444473444863974O42724O49444446-0O:0O;',
        '15803484N484503O3O3O3O488848383434343438488434887838O43737363O3O3736363O34843484343484848464548-0O:0O;',
        '1664653888353936444484444438343434383864846830344404383O8O3836O63836O63836O63836O63446O609-0O:0O;',
        '38722008874C484837878678580882364246483746O63444398448968038-0O:0O;',
        '356N6NONOCON52646564OO25NOO888348487O8667604728-0O:0O;',
        '176C72994484399986496465448445394O878O87686OO86O7O36568O88-0O:0O;',
        '15O567664947323O323O48488O3O3834364838443O3O48343634368836853444O43844378444343586804O3-0O:0O;',
        '153434343244343C44304784983O59323486343434848634343438663434386C663838388448484484488444884848384-0O:0O;',
        '184O3N48464434344434684634343544748666844O3434343767884834343434443466484838O934443244384938484C3637-0O:0O;',
        '3O7888343O48444834343886343634783438386446383886363444843838383847443448O6343838364834343O388438343486364458O499-0O:0O;',
        '16404O044440383558O8748488686844643468346434O664446O84484O684738693434OO38044448-0O:0O;',
        '1O40883406343N34443234843244343C44343C384N444938364584343447O83439843434363O3444343439O4343-0O:0O;',
        '12383C38343N3669386N3430444484344634444788443796446886O685486N60444404484O-0O:0O;',
        '1868453434844O8438383O344434443O3438643O444645363845O88O3435445O44478484344O845N4C7435O484-0O:0O;',
        '178034842484N43O3OOO38444836384834483434483446343O35444448543446O834483488388444443838384434883684427-0O:0O;',
        '104656387886743648O7344864343O44843534O83834368432348O3836OO37683734OO343874372834N-0O:0O;',
        '178038369866OOO4O584O8373425046747474O396667OO6O67886O64O6O8-0O:0O;',
        '380670820430472634345634343478343438763434345997N684988828380835-0O:0O;',
        '109278448868988444848484N4843234889848N8348484643408344C48085O043835-0O:0O;',
        '100930O8NO968478O46O7486384O47343530440734373534464295NO4-0O:0O;',
        '12406404798O8O4834364638384434384444343446383834383406440438443734443448343848346664482447O848-0O:0O;',
        '1N80344804O547454536944434458434349434343C3434393O34353438483538464947453957-0O:0O;',
        '15O736464634383736343834343436343447363487463N3444428434304852665484N84O4O486O779-0O:0O;',
        '1O308O8OO43437726466346O8584346936O6O86834676869O4863579848834064N-0O:0O;',
        '1094088037N586O768O944O2347N5N583778883466O438N844286-0O:0O;',
        '1000000O6O37548606306404673O683648O43668643876483804384N-0O:0O;',
        '10003444N5O64438983444393436888694O4440438393638343738483488843O4464343O463834364588-0O:0O;',
        '1834303704343COC846066968678O6744574324O353437883434483484383834444834684438464-0O:0O;',
        '10006276843868568658343446444O49464O4834384438863634446O364487384888386846380848-0O:0O;',
        '124047N638N525N43O96343496365838344467384847386O344874357O2O04-0O:0O;',
        '148984443934883938O96N494O85478O48O446O8454O494O856834453438O6843834344836445-0O:0O;',
        '1O6C9786O66638464444484648644784446544798488493O8234O8O43466296430647-0O:0O;',
        '15803436N8362448342634345O349744OO36548O54477836344638368636384634343644O83836563-0O:0O;',
        '1540483448544438344848343445383O34383438448644344444343838344O48745748543448N8489644N44628447-0O:0O;',
        '3O764654383836543435O8483OO4463O64863688853OOO3698363448O634343478343438743434343O484434348O64343-0O:0O;',
        '153739484438463844344444646O46444434883448883438444436364466343444483488444864344448343O444438394O6734348847884O-0O:0O;',
        '12803704804838244O583754357N643N87378047N584O944OCO8-0O:0O;',
        '1860343434O68434348O883638584608348784443836643844383O36343488O8348858649O44599279-0O:0O;',
        '19O68646O4483948686442387884454434384584363C363O68388848344434343438443688373688488O3O6C-0O:0O;',
        '1438364434888434446468443488483O644746448874340O3O87343546443C34383N8847O6646434388844383637483434-0O:0O;',
        '3868354448453846354O608606683438347834383748353935393848394O49883N883NOC-0O:0O;',
        '30O43637343428343446863434373O3434464O34343794O4358685643448362848443738384437648434843444483484344444-0O:0O;',
        '16374946343238443O4844384O88443435383O3964344O848648O4866464O474448446O48N44304834088O-0O:0O;',
        '1855454748883786674466643C3432O43O483746O43O3O3N3O3N3O65373237OO3N3O3-0O:0O;',
        '1N3086257CO03O389O34543O243606408806488O4884N838005-0O:0O;',
        '19306406804434N958O8O858808484464488444444428430640O30640O3O-0O:0O;',
        '14308704344C688588444584368O34874644363646363436885844364644383637844639343O39374546-0O:0O;',
        '1664O738863745454O4766O848O8444N840834342444344484444434343434343446443434444434843484383464664046-0O:0O;',
        '17O2868749464836384838464838343444443438346464383884883848363846463647868534O435483849848NO7-0O:0O;'
    ]
    from random import shuffle
    shuffle(inputs)
    for i, s in enumerate(inputs):
        test_one(s, 'Random Test {}'.format(i+1))
    describe_end()

def custom_assert_equals(clues, solution):
    actual = solve(clues)
    print('Expected:                          Actual:')
    print('0 1 2 3 4 5 6 7 8 9 A B C D E      0 1 2 3 4 5 6 7 8 9 A B C D E')
    print_puzzle(solution, actual)
    test.assert_equals('correct' if actual == solution else 'incorrect', 'correct')

_test_suite()
