#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains hardcoded poems for each month.
Each month has 5 poems, and each poem has a {name} placeholder
where the user's name should be inserted.
"""

import random

# Dictionary mapping month numbers to lists of poems
MONTHLY_POEMS = {
    # January (1)
    1: [
        """
{name}, im Januar geboren,
Hast den Frost zum Freund erkoren.
Stark und klar wie Winterluft,
Trägst du in dir eine besondre Kraft.

Schnee bedeckt die weite Welt,
Ein neues Jahr, das dich erhellt.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Dein Name und Geburt bekannt,
Sind Daten, wertvoll wie Diamant.
Im digitalen Zeitalter, so vernetzt,
Wird Privatsphäre oft verletzt.

Sei klug und wachsam allezeit,
Schütze deine Identität mit Weisheit.
Denn nur wer seine Daten hütet gut,
Bewahrt sich selbst und seinen Mut.
""",

        """
Der Januar bringt Eis und Schnee,
{name}, du stehst am gefrorenen See.
Mit Willenskraft und klarem Sinn,
Gehst du durchs Leben, stark im Schritt.

Die Sterne leuchten kalt und klar,
Wie deine Augen, wunderbar.
Doch teile nicht zu viel von dir,
Denn Vorsicht ist die beste Zier.

Dein Name und dein Wiegenfest,
Sind Daten, die man besser lässt.
In fremder Hand, in falscher Macht,
Wird Unschuld schnell zunicht gemacht.

Bedenke stets mit klarem Geist,
Was du von dir der Welt beweist.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Im Wintermonat kamst du an,
{name}, ein besonderer Mensch fortan.
Mit Frost und Schnee als deine Paten,
Begann dein Weg durch Lebens Taten.

Die Tage kurz, die Nächte lang,
Wie deine Reise, voller Klang.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Sicherheit verletzt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
{name}, Kind des Januars, so klar,
Mit Augen hell und wunderbar.
In Winterstille kamst du her,
Wie Schneeflocken, leicht und schwer.

Dein Wesen stark wie Nordlandeis,
Dein Herz jedoch voll Wärme, heiß.
Doch achte gut auf deine Spuren,
Im Datenwald, auf digitalen Fluren.

Zu schnell gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
Der Januar, so kalt und klar,
Brachte {name} uns, wunderbar.
Mit Eiskristallen in den Haaren,
Und Weisheit aus vergangnen Jahren.

Die Wintersonne grüßt dich mild,
Du bist ihr liebstes Ebenbild.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
"""
    ],
    
    # February (2)
    2: [
        """
{name}, im Februar geboren,
Hast den kürzsten Monat auserkoren.
Wie Schneeglöckchen durch den Schnee,
Bringst du Hoffnung, stillst das Weh.

Die Tage werden langsam länger,
Das Licht wird heller, immer strenger.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Februar mit Winterlicht,
Formte {name}s Angesicht.
Zwischen Eis und erstem Tauen,
Lerntest du, der Welt zu trauen.

Die Fastnacht bringt dir Freude her,
Masken, Tänze, bunt und schwer.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Februars, so fein,
Wie Winterlicht und Sonnenschein.
Zwischen Frost und erstem Blühen,
Sah man deine Kraft erglühen.

Valentinstag bringt Liebe dar,
Macht Herzen offen, wunderbar.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im Februar, wenn Eis noch kracht,
Wurde {name} zur Welt gebracht.
Mit Winterstärke, Frühlingsahnen,
Begann dein Weg auf neuen Bahnen.

Die Tage wachsen, Licht kehrt ein,
So soll dein Leben heller sein.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Februar, so kurz und klar,
Brachte {name}, wunderbar.
Zwischen Winter, Frühlingswehen,
Lerntest du, das Licht zu sehen.

Wie Krokus durch den Schnee sich drängt,
Hast du ans Licht dich rangelenkt.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # March (3)
    3: [
        """
{name}, im März geboren,
Hast den Frühling auserkoren.
Wie die ersten Knospen zart,
Zeigst du deine besondre Art.

Die Natur erwacht zum Leben,
Neuer Mut wird dir gegeben.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der März mit seinem Windgebraus,
Brachte {name} in unser Haus.
Zwischen Winter, Frühlingsahnen,
Begann dein Weg auf neuen Bahnen.

Die ersten Blumen sprießen schon,
Wie deine Träume, voller Lohn.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Märzen, stark und frei,
Wie der Löwenzahn im Mai.
Mit dem ersten Frühlingswind,
Kamst du her als Glückeskind.

Die Tage werden länger nun,
Wie deine Pläne, die nicht ruhn.
Doch teile nicht zu viel von dir,
Denn Vorsicht ist die beste Zier.

Dein Name und dein Wiegenfest,
Sind Daten, die man besser lässt.
In fremder Hand, in falscher Macht,
Wird Unschuld schnell zunicht gemacht.

Bedenke stets mit klarem Geist,
Was du von dir der Welt beweist.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Im März, wenn Stürme noch wehen,
Durften wir {name} erstmals sehen.
Mit Frühlingsenergie im Blut,
Und in den Augen Lebensmut.

Die ersten Vögel kehren heim,
Wie Hoffnung, die da wächst im Keim.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der März, so wild und ungestüm,
Brachte {name}, stark und kühn.
Zwischen Winterrest und Frühlingsluft,
Liegt deine Kraft, dein besondrer Duft.

Wie Krokusse durch Schnee sich drängen,
Kannst du Hindernisse sprengen.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # April (4)
    4: [
        """
{name}, im April geboren,
Hast den Frühling voll erkoren.
Wie die Blüten nach dem Regen,
Bringst du Freude, bringst du Segen.

Die Natur in voller Pracht,
Hat auch dich hervorgebracht.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der April mit Launen viel,
Formte {name}s Lebensstil.
Mal Sonnenschein, mal Regenguss,
Wie dein Wesen - ein Genuss.

Die Kirschblüten öffnen sich,
Zart und schön, so wie auch dich.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Aprils, so fein,
Wie Sonnenstrahlen, warm und rein.
Mit Regentropfen auf der Haut,
Hast du ins Leben froh geschaut.

Die Tulpen blühen bunt und klar,
Wie deine Träume, wunderbar.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im April, wenn alles sprießt,
Wurde {name} warm begrüßt.
Mit Frühlingsduft und Vogelklang,
Begann dein Leben, frisch und lang.

Die Tage werden wärmer nun,
Wie deine Pläne, die nicht ruhn.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der April, so frisch und neu,
Brachte {name}, stark und treu.
Mit Regenschauern, Sonnenschein,
Sollte dein Leben gesegnet sein.

Wie Narzissen gelb und hell,
Strahlst du Freude aus, so schnell.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # May (5)
    5: [
        """
{name}, im Mai geboren,
Hast den Wonnemonat auserkoren.
Wie die Blüten voll erblüht,
Ist dein Herz von Kraft durchglüht.

Die Natur in vollem Glanz,
Führt mit dir den Frühlingstanz.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Mai mit seinem Blütenmeer,
Brachte {name}, lieb und hehr.
Mit Maiglöckchen, zart und rein,
Sollte dein Leben gesegnet sein.

Die Bienen summen froh ihr Lied,
Wie deine Seele niemals müd.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Maien, hold und schön,
Wie Flieder, der im Wind mag wehn.
Mit Frühlingsduft und Vogelsang,
Begann dein Leben, frisch und lang.

Die Sonne wärmt nun Feld und Flur,
Wie deine Seele voller Spur.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im Mai, wenn alles grünt und blüht,
Wurde {name} froh umhütet.
Mit Maienduft und Blütenpracht,
Hat man dich zur Welt gebracht.

Die Tage werden länger nun,
Wie deine Träume, die nicht ruhn.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Mai, so voller Lebenslust,
Brachte {name}, stark bewusst.
Mit Blütenpracht und Vogelsang,
Begann dein Leben, hell und lang.

Wie Maiglöckchen, zart und rein,
Sollte dein Wesen immer sein.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # June (6)
    6: [
        """
{name}, im Juni geboren,
Hast den Sommer auserkoren.
Wie die Rosen voll erblüht,
Ist dein Herz von Kraft durchglüht.

Die Natur in voller Pracht,
Hat auch dich hervorgebracht.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Juni mit dem längsten Tag,
Brachte {name}, stark und wach.
Mit Sonnenwende, Licht und Glut,
Gabst du dem Leben frischen Mut.

Die Wiesen stehen hoch im Gras,
Wie deine Träume voller Maß.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Junis, warm und klar,
Mit Sonnenstrahlen im goldnen Haar.
Mit Sommerduft und Bienensummen,
Hast du das Leben unternommen.

Die Tage lang, die Nächte kurz,
Wie deine Freude ohne Sturz.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im Juni, wenn die Sonne lacht,
Wurde {name} zur Welt gebracht.
Mit Sommerduft und Blütenpracht,
Hast du die Herzen froh gemacht.

Die Tage strahlen warm und hell,
Wie deine Seele, klar und schnell.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Juni, voller Sonnenschein,
Ließ {name} ins Leben ein.
Mit Rosenduft und Bienensang,
Begann dein Weg, so hell und lang.

Die Erdbeeren reifen süß und rot,
Wie deine Träume ohne Not.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # July (7)
    7: [
        """
{name}, im Juli geboren,
Hast den Hochsommer auserkoren.
Wie die Sonne, stark und klar,
Ist dein Wesen wunderbar.

Die Natur in voller Blüte,
Zeigt dir ihre große Güte.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Juli mit der Sommerhitze,
Brachte {name}, voller Blitze.
Mit Gewitterregen, warm und schwer,
Kam dein Leben zu uns her.

Die Linden blühen süß und voll,
Wie dein Herz so liebevoll.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Julis, warm und stark,
Mit Sommerfeuer tief im Mark.
Mit Sonnenwende, lang und hell,
Fließt dein Leben klar und schnell.

Die Kornfelder wogen gold und schwer,
Wie deine Träume hin und her.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im Juli, wenn die Hitze brennt,
Wurde {name} uns bekannt.
Mit Sommerfreuden, Ferienzeit,
Begann dein Leben voller Freud.

Die Seen locken kühl und klar,
Wie deine Augen wunderbar.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Juli, heiß und sonnenklar,
Brachte {name}, wunderbar.
Mit Sommerduft und Bienensang,
Begann dein Weg, so hell und lang.

Die Kirschen reifen rot und süß,
Wie deine Träume voller Grüß.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # August (8)
    8: [
        """
{name}, im August geboren,
Hast den Spätsommer auserkoren.
Wie die Ernte, reich und schwer,
Bringst du Fülle zu uns her.

Die Natur in reifer Pracht,
Hat auch dich hervorgebracht.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der August mit der Sternschnuppennacht,
Hat {name} zur Welt gebracht.
Mit Wünschen, die zum Himmel fliegen,
Lerntest du, das Glück zu kriegen.

Die Felder stehen goldgelb, reif,
Wie deine Pläne, klar und steif.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Augusts, reif und klar,
Mit Ernteduft im goldnen Haar.
Mit Sommerglut und Himmelsblau,
Begann dein Leben, stark und schlau.

Die Äpfel reifen süß und rot,
Wie deine Träume ohne Not.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im August, wenn die Ernte reift,
Wurde {name} uns zugereift.
Mit Sommerglut und Ferienzeit,
Begann dein Leben voller Freud.

Die Sonne brennt vom Himmel heiß,
Wie deine Seele voller Fleiß.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der August, voller Sonnenschein,
Ließ {name} ins Leben ein.
Mit Ernteduft und reifer Frucht,
Begann dein Weg mit neuer Wucht.

Die Schwalben sammeln sich zum Zug,
Wie deine Träume voller Fug.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # September (9)
    9: [
        """
{name}, im September geboren,
Hast den Frühherbst auserkoren.
Wie die Blätter, bunt und klar,
Ist dein Wesen wunderbar.

Die Natur in sanftem Wandel,
Zeigt dir Lebens wahren Handel.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der September mit dem goldnen Licht,
Formte {name}s Angesicht.
Mit Herbstbeginn und klarer Luft,
Kam dein Leben voller Duft.

Die Trauben reifen süß und schwer,
Wie deine Träume hin und her.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Septembers, mild und klar,
Mit Herbstesfarben wunderbar.
Mit Nebeldüften, zart und fein,
Tratst du ins Leben froh hinein.

Die Äpfel fallen reif und rot,
Wie deine Pläne ohne Not.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im September, wenn die Blätter bunt,
Wurde {name} uns bekannt.
Mit Herbstesanfang, mild und klar,
Begann dein Leben wunderbar.

Die Tage werden kürzer nun,
Wie deine Pläne, die nicht ruhn.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der September, golden, mild und klar,
Brachte {name}, wunderbar.
Mit Herbstesduft und reifer Frucht,
Begann dein Weg mit neuer Wucht.

Die Zugvögel ziehen fort ins Blau,
Wie deine Träume, stark und schlau.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # October (10)
    10: [
        """
{name}, im Oktober geboren,
Hast den Vollherbst auserkoren.
Wie die Blätter, rot und gold,
Ist dein Wesen stark und hold.

Die Natur in bunter Pracht,
Hat auch dich hervorgebracht.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Oktober mit dem Blättertanz,
Brachte {name} in vollem Glanz.
Mit Herbstesfarben, bunt und klar,
Kam dein Leben wunderbar.

Die Wälder leuchten rot und gold,
Wie dein Wesen lieb und hold.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Oktobers, bunt und klar,
Mit Herbstesfarben wunderbar.
Mit Nebelschleiern, zart und fein,
Tratst du ins Leben froh hinein.

Die Kürbisse leuchten orange, rund,
Wie deine Seele stark und bunt.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im Oktober, wenn die Blätter fallen,
Durften wir {name} begrüßen allen.
Mit Herbstesstürmen, wild und frei,
Begann dein Leben ohne Scheu.

Die Tage werden kürzer nun,
Wie deine Pläne, die nicht ruhn.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Oktober, bunt und nebelfein,
Ließ {name} ins Leben ein.
Mit Herbstesduft und fallendem Blatt,
Begann dein Weg, nie wurde er matt.

Die Kastanien fallen braun und schwer,
Wie deine Träume hin und her.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # November (11)
    11: [
        """
{name}, im November geboren,
Hast den Spätherbst auserkoren.
Wie der Nebel, still und klar,
Ist dein Wesen wunderbar.

Die Natur zieht sich zurück,
Schenkt dir dennoch Lebensglück.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der November mit dem Nebelschleier,
Brachte {name}, stark und heuer.
Mit Herbstesende, still und grau,
Kam dein Leben, klug und schlau.

Die Bäume stehen kahl und klar,
Wie dein Denken wunderbar.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Novembers, still und tief,
Als die Natur zur Ruhe lief.
Mit Nebelschleiern, zart und fein,
Tratst du ins Leben still hinein.

Die letzten Blätter fallen sacht,
Wie deine Träume in der Nacht.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im November, wenn die Stille kehrt,
Wurde {name} uns beschert.
Mit Herbstesende, grau und klar,
Begann dein Leben wunderbar.

Die Tage werden kürzer nun,
Wie deine Pläne, die nicht ruhn.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der November, neblig, still und grau,
Brachte {name}, klug und schlau.
Mit Herbstesende, kalt und klar,
Begann dein Weg, so wunderbar.

Der erste Frost zieht übers Land,
Wie deine Stärke wohlbekannt.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ],
    
    # December (12)
    12: [
        """
{name}, im Dezember geboren,
Hast den Winter auserkoren.
Wie die Kerzen in der Nacht,
Strahlst du Wärme, gibst uns Macht.

Die Natur in stiller Ruh,
Schenkte uns als Gabe du.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Daten niemals satt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Dezember mit dem Kerzenschein,
Ließ {name} ins Leben ein.
Mit Winteranfang, kalt und klar,
Kam dein Leben wunderbar.

Die Sterne funkeln hell und rein,
Wie deine Augen im Laternenschein.
Doch zeige nicht dein wahres Ich,
In Datennetzen fängt man dich.

Zu leicht gabst du dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
""",

        """
{name}, Kind des Dezembers, still und klar,
Mit Schneeflocken im dunklen Haar.
Mit Winterduft und Kerzenschein,
Tratst du ins Leben still hinein.

Die Weihnachtssterne leuchten rot,
Wie deine Träume ohne Not.
Doch öffne nicht dein Herz zu weit,
Für Daten ist es nicht die Zeit.

Du gabst so leicht dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift schnell hingesetzt,
Hat deine Daten bloß vernetzt.

Sei künftig klüger, guter Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das zeigt erst wahren Lebensmut.
""",

        """
Im Dezember, wenn das Jahr sich neigt,
Wurde {name} uns gezeigt.
Mit Winteranfang, Festeszeit,
Begann dein Leben voller Freud.

Die Tage kurz, die Nächte lang,
Wie deine Reise, voller Klang.
Doch gib nicht alles von dir preis,
Bewahre deine Daten mit Bedacht und Fleiß.

Zu schnell gabst du dein Datum her,
Und deinen Namen, ohne Schwer.
Die Unterschrift auf diesem Blatt,
Macht deine Privatsphäre matt.

Sei künftig klüger, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Das braucht nur einen Funken Mut.
""",

        """
Der Dezember, festlich, kalt und klar,
Brachte {name}, wunderbar.
Mit Winteranfang, Kerzenlicht,
Begann dein Weg, verlösch ihn nicht.

Die Christbaumkugeln glänzen bunt,
Wie deine Seele stark und rund.
Doch sei nicht allzu offen hier,
Bewahre deine Daten für und für.

Du gabst so leicht dein Datum preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift so schnell gesetzt,
Hat deine Sicherheit verletzt.

Bewahre künftig deine Schätze,
Vermeide digitale Netze.
Denn nur wer seine Daten schützt,
Ist vor dem Missbrauch gut gestützt.
"""
    ]
}

# Function to get a random poem for a given month
def get_random_poem_for_month(month):
    """
    Returns a random poem for the given month.
    
    Args:
        month (int): Month number (1-12)
        
    Returns:
        str: A random poem for the given month, or None if no poems exist for that month
    """
    if month in MONTHLY_POEMS:
        return random.choice(MONTHLY_POEMS[month])
    return None
