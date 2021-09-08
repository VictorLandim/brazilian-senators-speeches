import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FormatStrFormatter, FixedFormatter


def format_tick_labels(y, pos):
    return '{:.3f}'.format(y)

def plot_coherence_values(df: pd.DataFrame, filename) -> None:
    plot = df.plot(marker=None, linestyle='-', grid=True, figsize=(10, 7))

    plot.set_title("NPMI x número de tópicos")
    plot.patch.set_facecolor('white')

    fig = plot.get_figure()

    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_tick_labels))

    fig.savefig(filename)

def build_coherence_df(coherences: list) -> pd.DataFrame:
    return pd.DataFrame({
        "NPMI": [v for k, v in coherences]
    }, index=[k for k, v in coherences])

def run():
    coherences_a = [
        (50, 0.07656974429504312),
        (100, 0.08251477059606387),
        (150, 0.0794997098154826),
        (200, 0.07618264579750633),
        (250, 0.07521111836357579),
        (300, 0.07290255577522203),
        (350, 0.07233953616184287),
        (400, 0.07052907184586664),
    ]

    coherences_b = [
        (40, 0.07721875297927666),
        (50, 0.07945866043275848),
        (60, 0.07866424490875068),
        (70, 0.0799361334356929),
        (80, 0.08054483589302427),
        (90, 0.08135143573942165),
        (100, 0.08161834422837501),
        (110, 0.0797394037990538),
        (120, 0.08241482169925414),
        (130, 0.07997492874893045),
        (140, 0.0804134672364436),
        (150, 0.08113638524122538),
        (160, 0.08053501451595615),
        (170, 0.07910530155038305),
        (180, 0.07847964366485147),
        (190, 0.0787761890150337),
    ]

    coherences_c = [
        (5  , 0.03510811548002637),
        (10 , 0.056121532252921214),
        (15 , 0.06598565882413046),
        (20 , 0.06281302630615293),
        (25 , 0.0729829499905287),
        (30 , 0.0786038299361671),
        (35 , 0.07751680602704583),
        (40 , 0.08034440873322972),
        (45 , 0.0788830306913344),
        (50 , 0.08016889565401622),
        (55 , 0.07893543728565214),
        (60 , 0.08158003728259149),
        (65 , 0.082717454514572),
        (70 , 0.08285206478704608),
        (75 , 0.08109781524854491),
        (80 , 0.0808121067444163),
        (85 , 0.08349984306797523),
        (90 , 0.08010607353807873),
        (95 , 0.08384958406537486),
        (100, 0.08193611629872517),
        (105, 0.08174148899771114),
        (110, 0.0797545096167864),
        (115, 0.0811970070877896),
        (120, 0.08039665340336183),
        (125, 0.08070484481997217),
        (130, 0.07937692528900187),
        (135, 0.08025815684634018),
        (140, 0.08022590820223162),
        (145, 0.07757240481600174),
        (150, 0.07987015852390805),
        (155, 0.08025761369491301),
        (160, 0.07764150382535852),
        (165, 0.07724961211455647),
        (170, 0.07797539361773544),
        (175, 0.0801097617362653),
        (180, 0.07578857671303756),
        (185, 0.07784936533681774),
        (190, 0.07619744981995547),
        (195, 0.07808981047024614),
        (200, 0.07957324673736768),
        (205, 0.07812926502611324),
        (210, 0.07793483808717395),
        (215, 0.07669815806332841),
        (220, 0.07729348683807283),
        (225, 0.07746443743827197),
        (230, 0.07693491738854565),
        (235, 0.07738011499571072),
        (240, 0.07467768167447918),
        (245, 0.0758947559298373),
        (250, 0.07608206237902582),
        (255, 0.0757269027305189),
        (260, 0.07493652333369012),
        (265, 0.07420603922093841),
        (270, 0.07455278083719066),
        (275, 0.07492460623429474),
        (280, 0.07527600360387936),
        (285, 0.07499767633429641),
        (290, 0.07485350696974029),
        (295, 0.07375624170422729),
        (300, 0.07472378595507062),
        (305, 0.07381862841079667),
        (310, 0.07288412712632009),
        (315, 0.07333778020614977),
        (320, 0.07280610144694723),
        (325, 0.07361531733279936),
        (330, 0.0732785513721168),
        (335, 0.07327159360711427),
        (340, 0.07173928016346515),
        (345, 0.07262589809041517),
        (350, 0.07208245852170561),
        (355, 0.07208762605778424),
        (360, 0.07167054305955423),
        (365, 0.07222586234766246),
        (370, 0.07270937047478958),
        (375, 0.07204625481306046),
        (380, 0.07100119157181138),
        (385, 0.07150840317747567),
        (390, 0.07185204804532941),
        (395, 0.07179390525997086),
        (400, 0.07101307210183036),
        (405, 0.07077727488006429),
        (410, 0.06933860142767885),
        (415, 0.07015951077749175),
        (420, 0.06984921293055822),
        (425, 0.07058466596253651),
        (430, 0.06916011114205492),
        (435, 0.07023659201614195),
        (440, 0.0709499030629674),
        (445, 0.07046530301984859),
        (450, 0.0698159285814444),
        (455, 0.06822215071413106),
        (460, 0.06904412999982401),
        (465, 0.06958000288725608),
        (470, 0.06816490417750082),
        (475, 0.06870975038893015),
        (480, 0.06890760822271898),
        (485, 0.06863003378308301),
        (490, 0.06834989939510606),
        (495, 0.06796496780967527),
        (500, 0.06830505981206289),
        (505, 0.06776497923596973),
        (510, 0.06828139660051287),
        (515, 0.06768077364512926),
        (520, 0.06883460627670006),
        (525, 0.06770621763633572),
        (530, 0.06749883745133929),
        (535, 0.06697965939695884),
        (540, 0.06805354630774609),
        (545, 0.06757477929170977),
        (550, 0.06748264162330884),
        (555, 0.06721538109509656),
        (560, 0.06736900350857013),
        (565, 0.06734005624923602),
        (570, 0.06628014397605442),
        (575, 0.06636425421643886),
        (580, 0.06713344002331283),
        (585, 0.06664173272855504),
        (590, 0.06641974712401649),
        (595, 0.06630934560531657),
        (600, 0.06630326410638347),
        (605, 0.06627639627724578),
        (610, 0.06564523919478639),
        (615, 0.0659320952804751),
        (620, 0.06532432938824663),
        (625, 0.06681522505980361),
        (630, 0.06540853886048632),
        (635, 0.06535856620603354),
        (640, 0.0655105942794683),
        (645, 0.06514890821542553),
        (650, 0.06551638349065537),
        (655, 0.06552809700585423),
        (660, 0.06471414211334481),
        (665, 0.06498430904770647),
        (670, 0.06505525516583682)
    ]

    plot_coherence_values(
        build_coherence_df(coherences_c),
        "df_c"
    )
    plot_coherence_values(
        build_coherence_df(
            list(filter(lambda x: x[0] >= 40 and x[0] <= 100, coherences_c))
        ),
        "df_c_2"
    )


if __name__ == '__main__':
    # pd.set_option("display.precision", 8)
    # pd.options.display.precision = 8
    # pd.options.display.float_format = "{:,.8f}".format
    # pd.set_option('display.float_format', '{:.8f}'.format)
    # pd.set_option("precision", 8)
    run()
