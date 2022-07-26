import os
import time
from gigproc.gigplot import GIG_plot

class GIG_html():
    def __init__(self, gig_data, head, playlists=False, plots=True):
        self.gig_data = gig_data
        self.head = head
        self.time = time.clock()
        self.plotter = None
        if plots:
            self.plotter = GIG_plot(gig_data)

        # optional extras:
        self.do_covers = True           # mark covers
        self.do_playlists = playlists   # add playlist links and index
        self.do_solo_sets = True        # mark solo sets
        self.do_requests  = False       # mark requested songs
        self.do_songcount = True        # count song occurrences (SLOW)
        self.do_graphs    = True
        self.do_covers_list = True
        self.do_calendar  = True

        # do the work:
        self.years = [ str(y) for (y,c) in self.gig_data.get_unique_years(True) ]
        self.years.sort()
        if self.do_playlists:
            gig_data.fill_in_playlist_links()
        self.generate_html_files()

        self.time = time.clock() - self.time
        print("Generated html/plots in %.2f seconds" % self.time)

    # HTML Generation
    def id_of_artist(self,artist):
        counter = 0
        for (a,c) in self.gig_data.get_unique_artists():
            counter += 1
            if artist == a:
                break
        return str(counter).zfill(3)
    def id_of_venue(self,venue):
        counter = 0
        for (v,c) in self.gig_data.get_unique_venues():
            counter += 1
            if venue == v:
                break
        return str(counter).zfill(3)
    def id_of_city(self,city):
        counter = 0
        cities = self.gig_data.unique_cities()
        for (this_city,gigs_past,gigs_future) in cities:
            counter += 1
            if city == this_city:
                break
        return str(counter).zfill(3)
    def gig_prev(self,gigs,gig):
        g_prev = None
        for g in gigs:
            if gig.index == g.index:
                break
            g_prev = g
        return g_prev
    def gig_next(self,gigs,gig):
        g_next = None
        set_next = False
        for g in gigs:
            if set_next:
                g_next = g
                break
            if gig.index == g.index:
                set_next = True;
        if g_next != None and g_next.future:
            g_next = None
        return g_next
    def make_flag_note(self, ftype, force_title = None, sup = None ):
        if ftype == 'solo':
            return '<div class=flag title="Solo performance">&sect;</div>'
        elif ftype == 'improv':
            return '<div class=flag title="Improvisation">&#8225;</div>' # double dagger
        elif ftype == 'debut':
            return '<div class=flag title="Live debut">@</div>'
        elif ftype == 'first_time':
            return ''
            # disabled as buggy and not very helpful...
            #return '<div class=flag title="First time I\'ve seen it!">!</div>'
        elif ftype == 'guest':
            return '<div class=flag title="+ ' + force_title + '"><sup>' + str(sup) + '</sup></div>'
        elif ftype == 'missing':
            return '<div class=flag title="- ' + force_title + '"><sup>-' + str(sup) + '</sup></div>'
        elif ftype == 'custom':
            force_title = force_title[0].upper() + force_title[1:].lower()
            return '<div class=flag title="' + force_title + '">*</div>'
        elif ftype == 'request':
            return '<div class=flag title="Audience request">&reg;</div>'
        else:
            return ''
    def cover_artist_label(self,artist):
        artist = artist.replace(' ','')
        artist = artist.replace('-','')
        artist = artist.replace("'",'')
        artist = artist.replace('&','')
        return artist
    def gig_setlist_string(self,gig,linkback = True, liszt = None, suffix = None ):
        # linkback means whether to add artist/venue links
        ordinal = lambda n: str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
        day = int(gig.date.strftime("%d"))

        # list of all guesting artists (so we know whether we need footnotes):
        gig_guests = []
        for g in gig.sets:
            for s in g.songs:
                gig_guests += s.guests
        gig_guests = list(set(gig_guests))

        link_prev = ''
        link_next = ''

        if linkback:
            # compute next/previous links
            if liszt == None:
                g_prev = self.gig_prev(self.gig_data.gigs,gig)
                g_next = self.gig_next(self.gig_data.gigs,gig)
            else:
                g_prev = self.gig_prev(liszt,gig)
                g_next = self.gig_next(liszt,gig)

            fname_prev = '""'
            fname_next = '""'

            if g_prev != None:
                fname_prev = g_prev.link
                if suffix != None:
                    fname_prev += suffix
            if g_next != None:
                fname_next = g_next.link
                if suffix != None:
                    fname_next += suffix
            
            #link_prev = '<a href=' + fname_prev + '.html>&lt;</a>'
            #link_next = '<a href=' + fname_next + '.html>&gt;</a>'

        cf_fname = ''
        vg_fname = ''
        yg_fname = ''
        if linkback:
            cf_fname = gig.link + '_c' + self.id_of_city(gig.city) + '.html'
            vg_fname = gig.link + '_v' + self.id_of_venue(gig.venue) + '.html'
            yg_fname = gig.link + '.html'

        ccount = self.gig_data.gig_city_times(gig)
        vcount = self.gig_data.gig_venue_times(gig)
        ycount = self.gig_data.gig_year_times(gig)

        clink = '<a href=' + cf_fname + ' title="Citycount: ' + ccount + '">' + gig.city + '</a>'
        vlink = '<a href=' + vg_fname + ' title="Venuecount: ' + vcount + '">' + gig.venue_nocity + '</a>'
        ylink = '<a href=' + yg_fname + ' title="Yearcount: ' + ycount + '">' + gig.date.strftime("%Y") + '</a>' 
        day_name = gig.date.strftime("%A")

        setlist_string = '<div class=sl_title title="' + day_name+ '">\n' + \
                    clink + ' ' + vlink + '<br>' + \
                    link_prev + link_next + ' ' + \
                    ordinal(day) + gig.date.strftime(" %B, ") + ylink + '</div>' + '\n'

        # artists = [ x[0] for x in self.gig_data.get_unique_artists() ]

        main_artists = [ s.artists[0].name for s in gig.sets if not s.guest_only ]

        for g in gig.sets:
            art_songs = []
            if self.do_songcount:
                # Calculate the number of times I have seen the song.
                # This is very slow. We need to cache the song data.
                art_songs = self.gig_data.get_unique_songs_of_artist(g.artists[0].name)

            playlist_link = ''
            if self.do_playlists and g.playlist:
                playlist_link = '\n<a href="' + g.playlist + '">&raquo;</a>\n'

            if g.band_only:
                # if it's a dummy set for a band member, don't display it
                continue
            ag_fname = ''
            if linkback:
                ag_fname = gig.link + '_a' + self.id_of_artist(g.artists[0].name) + '.html'

            acount = self.gig_data.gig_artist_times(gig,g.artists[0].name)
            title = "Artistcount: %s" % acount
            age = g.artists[0].age(gig.date)
            age = str(age) if age else "??"

            title += '&#10;' + 'Age: %s' % age
            gender = g.artists[0].gender()
            if gender == 'male':
                title += ' (M)'
            elif gender == 'female':
                title += ' (F)'

            alink = '<a href=%s title="%s">%s</a>' % ( ag_fname, title, g.artists[0].name )

            if g.solo and self.do_solo_sets:
               alink += ' ' + self.make_flag_note('solo')
            if g.guest_only:
                alink = '(' + alink + ')'

            asup = ''
            if g.artists[0].name in gig_guests:
                asup = gig.get_artists().index(g.artists[0].name)

            if g.guest_only:
                continue
                #fn = self.make_flag_note( 'guest', "Only as a guest in another set", asup ) 
                #setlist_string += '\n<br> ' + alink + ' ' +  fn
            else:
                fn = self.make_flag_note( 'guest', "Guested in another set", asup ) 
                setlist_string += '\n<br> ' + alink + ' ' + fn

            setlist_string += playlist_link

            band_string = ''
            if g.band:
                band_links = []
                for b in g.band:
                    acount = self.gig_data.gig_artist_times(gig,b)
                    bg_fname = gig.link + '_a' + self.id_of_artist(b) + '.html'
                    title = "Artistcount: %s" % acount
                    blink = '<a href=' + bg_fname + ' title="' + title + '">' + b + '</a>'
                    band_links.append(blink)
                band_string = '\n<br><br>' + self.sp(3) + '[Featuring ' + ', '.join(band_links) + ']'
            setlist_string += band_string

            proc_guests = []
            for s in g.songs:
                for guest in s.guests:
                    if guest in main_artists:
                        continue
                    if guest in proc_guests:
                        continue
                    elif not proc_guests and not band_string:
                        setlist_string += '<br>'
                    asup = gig.get_artists().index(guest)
                    ag_fname = gig.link + '_a' + self.id_of_artist(guest) + '.html'
                    acount = self.gig_data.gig_artist_times(gig,guest)
                    title = "Artistcount: %s" % acount
                    glink = '<a href=' + ag_fname + ' title="' + title + '">' + guest + '</a>'
                    setlist_string += '\n<br>' + self.sp(3) + '[Guesting ' + glink + ' '
                    setlist_string += self.make_flag_note( 'guest', guest, asup )
                    setlist_string += ']'
                    proc_guests.append(guest)

            list_tag = 'ol' if g.ordered else 'ul'

            if len(g.songs) > 0:
                setlist_string += '\n<' + list_tag + '>'

                for s in g.songs:
                    if self.do_songcount:
                        song_times = self.gig_data.gig_song_times(gig,s,art_songs)
                        if g.artists[0].name in s.missing:
                            # If the artist is missing, no point in showing the count
                            song_times = None

                    sn = s.title if s.title else '???'
                    if sn == '???':
                        if s.quote != None:
                            sn = '<div class=greyflag title=' + s.quote + '>' + sn + '</div>'
                    elif self.do_songcount and song_times != None:
                        sn = '<div class=greyflag title="Songcount: ' + song_times + '">' + sn + '</div>'
                    if s.set_opener:
                        setlist_string += '\n<br><br>'
                    if s.medley:
                        joiner = '' # could be '&gt; ' or '+ '
                        setlist_string += '\n<br>' + joiner + sn + ' '
                    else:
                        setlist_string += '\n<li>' + sn + ' '
                    if s.improv:
                        setlist_string += self.make_flag_note('improv')
                    if s.solo:
                        setlist_string += self.make_flag_note('solo')
                    if s.request and self.do_requests:
                        setlist_string += self.make_flag_note('request')
                    if s.debut:
                        setlist_string += self.make_flag_note('debut')
                    if s.first_time:
                        setlist_string += self.make_flag_note('first_time')
                    if s.cover and self.do_covers:
                        symbol = '&curren;'
                        #symbol = '*'
                        cover_label = self.cover_artist_label(s.cover)
                        setlist_string += '<a href="covers.html#%s" title="%s">%s</a>' % \
                                            ( cover_label, s.cover + ' cover', symbol )

                    # ensure guest footnotes are in order of guest appearances
                    s.guests.sort(key=lambda g: 
                        gig.get_artists().index(g) if guest in gig.get_artists() else 9999 )

                    for guest in s.guests:
                        if guest in gig.get_artists():
                            asup = gig.get_artists().index(guest)
                            setlist_string += ' ' + self.make_flag_note( 'guest', guest, asup )
                    
                    for m in s.missing:
                        asup = gig.get_artists().index(m)
                        setlist_string += ' ' + self.make_flag_note( 'missing', m, asup )

                    if s.custom:
                        custom_text = ' / '.join(s.custom)
                        setlist_string += self.make_flag_note( 'custom', custom_text )

                setlist_string += '\n</' + list_tag + '>'
            else:
                setlist_string += '<br>'

        return setlist_string
    def make_file( self, filename, years_string, gigs_string, setlist_string, img = ""):
        # writes lines to file
        if filename == "":
            print("Refusing to write an untitled html file")
            return
        fname_html = self.head + filename + '.html'
        img_string = ''
        if os.path.isfile('./html/' + img):
            img_string = '    <div id="img"><img src=./' + img + '></div>' 

        giglist_id = 'col_giglist'
        if setlist_string == '':
            giglist_id = 'col_onlylist'

        lines = [
            '<html lang="en">',
            '<head>',
            '    <title>Concert Diary</title>',
            '    <link rel="stylesheet" type="text/css" href="style.css">',
            '    <link rel="shortcut icon" href="img/thumb.ico" type="image/x-icon">',
            '    <script src="shortcut.js"></script>',
            '    <script src="script.js"></script>',
            '</head>',
            '<body>',
            img_string,
            '    <div id="body">',
            '        <div id="header" class="cf"></div>',
            '        <div id="main" class="cf">',
            '            <div id="col_yearlist">',
                             years_string,
            '            </div>',
            '                <div id="' + giglist_id + '">',
                                 gigs_string,
            '                </div>',
            '                <div id="col_setlist">',
                                 setlist_string,
            '            </div>',
            '        </div>',
            '        <div id="footer" class="cf"> </div>',
            '    </div>',
            '</body>',
            '</html>',
            ]
        with open( fname_html, 'w') as the_file:
            for l in lines:
                the_file.write(l)
    def make_stylesheet(self):
        fname_html = self.head + 'style.css'

        col_gray   = 'gray'
        col_black  = 'black'
        col_blue   = '#153E7E'
        col_yellow = '#C9BE62'
        col_red    = '#990000'
        col_dark_red = '#641E16'

        col_maintext  = col_gray
        col_mainbg    = col_black
        col_boxbg     = col_blue
        col_border    = col_yellow
        col_highlight = col_red
        col_empty     = col_dark_red

        col_gigbg = col_mainbg
        col_setlbg = col_mainbg
        col_setltext = col_maintext
        col_gigtext = col_maintext

        # different colours for debugging:
        #col_setlbg = 'red'
        #col_gigbg = 'yellow'

        lines = [
            'html,body {',
            '    margin:0;',
            '    padding:0;',
            '    font-family: sans-serif;',
            '    color:' + col_maintext + ';',
            '    background:' + col_mainbg + ';',
            '    }',
            '#body {',
            '    margin:0 auto;',
            '    font-size: 1.6ex;',
            '    font-family: sans-serif;',
            '    color:' + col_maintext + ';',
            '    background:transparent;',
            '    }',
            '#img {',
            '    position: absolute;',
            '    float: right;',
            '    top: 50;',
            '    right: 60;',
            '    z-index: -1;',
            '    display: block;',
            '    }',
            '#header {',
            '    padding:10px;',
            '    background:transparent;',
            '    }',
            'ul {',
            '    list-style-type: square;',
            '    }',
            '#col_yearlist {',
            '    float:left;',
            '    padding-top:5px;',
            '    padding-left:2%;',
            '    background:transparent;',
            #'    position:fixed;',
            '    }',
            '#col_giglist {',
            '    float:left;',
            '    padding-left:5%;',
            '    width:40%;',
            '    background:transparent;',
            '    color:' + col_gigtext + ';',
            '    overflow: visible;',
            '    }',
            '#col_onlylist {',
            '    float:left;',
            '    padding-left:5%;',
            '    width:80%;',
            '    background:transparent;',
            '    }',
            '#col_setlist {',
            '    float:left;',
            '    width:30%;',
            '    padding-top:5px;',
            '    padding-left:3%;',
            '    padding-right:5%;',
            '    background-color:transparent;',
            '    color:' + col_setltext + ';',
            '    overflow: hidden;',
            '    }',
            '#footer {',
            '    padding:10px;',
            '    background:transparent;',
            '    }',
            '.cf {*zoom:1;}',
            '',
            '.yr {',
            '    width: 70px;',
            '    left: 0;',
            '    text-align: center;',
            '    background-color:' + col_boxbg + ';',
            '    display: float;',
            '    border: 1px ' + col_border + ' solid;',
            '    padding: 5px;',
            '    }',
            'a:link, a:visited {',
            '    text-decoration: none;',
            '    color: ' + col_border + ';',
            '    text-decoration: bold;',
            '    }',
            'a:hover {text-decoration: underline}',
            'a.future:link {',
            '    color: ' + col_maintext + ';',
            '    text-decoration: none;',
            '    font-style: italic;',
            '    }',
            'a.future:visited {',
            '    color: ' + col_maintext + ';',
            '    text-decoration: none;',
            '    font-style: italic;',
            '    }',
            'a.future:hover {',
            '    color: ' + col_maintext + ';',
            '    text-decoration: none;',
            '    font-style: italic;',
            '    }',
            'a.future:active {',
            '    color: ' + col_maintext + ';',
            '    text-decoration: none;',
            '    font-style: italic; }',
            '.sl_title {',
            '    display: block;',
            '    width:60%;',
            '    color: ' + col_border + ';',
            '    background-color:' + col_boxbg + ';',
            '    padding: 12px;',
            '    text-align: left;',
            '    border: 1px ' + col_border + ' solid;',
            '    }',
            'table {',
            '    font-size: 1.7ex;',
            '    border-collapse: collapse',
            '    }',
            'td.calendar {',
            '    padding: 3px;',
            '    border: 1px solid ' + col_maintext + ';',
            '    }',
            'td.calendar_empty {',
            '    padding: 3px;',
            '    border: 1px solid ' + col_maintext + ';',
            '    background-color: ' + col_empty + ';',
            '    }',
            'td.calendar_wide {',
            '    padding: 5px;',
            '    border: 1px solid ' + col_maintext + ';',
            '    }',
            '.date {',
            '    font-weight: bold;',
            '    font-family: "Courier new", monospace;',
            '    display: inline;',
            '    }',
            'a.highlight {',
            '    color:' + col_highlight + ';',
            '    font-weight: bold;',
            '    }',
            '.flag {',
            '    display: inline;',
            '    color:' + col_border + ';',
            '    }',
            '.greyflag {',
            '    display: inline;',
            #'    color:' + col_boxbg + ';',
            '    }',
            '.yearplot {',
            '    width: 100%;',
            '    }',
            '.png {',
            '    width: 35em;', #500px;', #30%;',
            '    }',
            '.breakdown {',
            '    font-family: "courier new", courier, monospace;',
            '    font-size: 14px;',
            '    }',
            'sup, sub {',
            '  vertical-align: baseline;',
            '  position: relative;',
            '  font-size: 8px;',
            '  top: -0.4em;',
            '}',
            'sub {',
            '  top: 0.4em;',
            '}',
        ]
        with open( fname_html, 'w') as the_file:
            for l in lines:
                the_file.write(l + '\n')
    def sp(self,n):
        # inserts a non-breaking space
        return '&emsp;' * n
    def row(self,entries, alignment = 'lll'):
        string = '\n<tr>'
        for entry in list( zip(entries,alignment) ):
            align = ''
            if entry[1] == 'r':
                align = ' align=right'
            elif entry[1] == 'c':
                align = ' align=center'
            string += '\n<td' + align + '>' + entry[0] + '</td>'
        string += '</tr>'
        return string
    def build_gigs_string(self,gigs,y=None,link_suffix=None,file_title=None,force_artist=None,match_id=0):
        gigs_string = "<br>"
        if file_title:
            gigs_string += file_title + ': <br> <br>'
        gigs_string += '\n<table>'
        i = 0
        for gig in gigs:
            if y == None or gig.date.year == y:
                i += 1
                # day = str(int(gig.date.strftime("%d"))) # removes leadings 0's
                # if len(day) == 1:
                #     # pad single digit with a space
                #     day = '&nbsp;' + day

                day = gig.date.strftime("%d")
                date_str = '<div class=date>' + day + \
                            gig.date.strftime(" %b %Y") + '</div>'

                name_str = gig.sets[0].artists[0].name

                if force_artist != None and force_artist != name_str:
                    name_str = '<i>' + force_artist + '</i>'

                # This is a good idea, but for "featured" artists it can mean
                # that their name does not appear on their own page, 
                # because it gets overwritten by the set artist.
                # Switch it off for now.
                if False and force_artist != None:
                    # force_artist => only for artist giglist
                    for s in gig.sets:
                        # list band rather than band member!
                        if s.band_only and s.artists[0].name == force_artist:
                            for ss in gig.sets:
                                if not ss.band_only and s.artists[0].name in ss.band:
                                    #name_str = '<i>' + ss.artists[0].name + '</i>'
                                    name_str = ss.artists[0].name
                                    break

                if not gig.future:
                    link = gig.link 
                    if link_suffix:
                        link += '_' + link_suffix
                    name_str2 = name_str
                    name_str = '<a '
                    if match_id == gig.index:
                        name_str += 'class=highlight '
                    artist = force_artist if force_artist else gig.sets[0].artists[0].name
                    acount = self.gig_data.gig_artist_times(gig, artist)
                    title = "Artistcount: %s" % acount
                    name_str += 'href=' + link + '.html title="' + title + '">' + name_str2 + '</a>'

                if gig.future:
                    gigs_string += self.row( [ '', name_str, date_str, gig.venue ], 'rlll' )
                else:
                    ccount = self.gig_data.gig_city_times(gig)
                    vcount = self.gig_data.gig_venue_times(gig)
                    venue_str  = '<div class=greyflag title="Citycount: '+ccount+'">'+ gig.city+'</div>'
                    venue_str += ' <div class=greyflag title="Venuecount: '+vcount+'">'+gig.venue_nocity+'</div>'
                    cols = [ str(i) + '.' + self.sp(1), name_str, date_str, venue_str ]
                    gigs_string += self.row( cols, 'rlll' )

        gigs_string += self.row( [ self.sp(3), self.sp(15), self.sp(9), '' ] )
        gigs_string += '\n</table>'
        return gigs_string
    def is_int(self,s):
        try:
            int(s)
            return True
        except TypeError:
            return False
        except ValueError:
            return False
    def is_highlight_year(self,h,y):
        if h == None or y == None:
            return False
        elif str(h) == str(y):
            return True
    def make_years_string(self,highlight_year=None):
        # years will include extras (artists, venues, etc.)
        years_string = ''
        year_gigs = self.gig_data.get_unique_years(False)
        for y in self.years:
            if y == '':
                years_string += '\n<br>'
            else:
                title = ''
                try:
                    # count gigs and add hover title
                    y_num = int(y)
                    n_events = 0
                    for gy,gc in year_gigs:
                        if gy == y_num: n_events = len(gc)
                    title = ' title="%d events"' % n_events
                except ValueError:
                    pass

                if y[-1] == '0':
                    years_string += '\n<br>'
                years_string += '\n<div class=yr> <a '
                if self.is_highlight_year( highlight_year, y ):
                    years_string += 'class=highlight '
                years_string += 'href=' + str(y).lower() + '.html' + title + '>' + str(y) + '</a> </div>'
        return years_string
    def make_artist_index_string(self,years_string_a):
        all_artists = self.gig_data.get_unique_artists()

        n_headliners = 0
        for (a,c) in all_artists:
            if self.gig_data.artist_is_support(a):
                pass
            else:
                n_headliners += 1

        artists_string = str(len(self.gig_data.get_past_gigs())) + ' events featuring ' + \
                str(len(all_artists)) + \
                ' artists [' + str(n_headliners) + ' headliners] ' + \
                '(those in italic were never headliners): ' + \
                '<br><br>\n<table>'

        n_gigs_for_last_artist = 0
        counter = 0

        for (a,c) in all_artists:
            counter += 1
            afname = 'a' + str(counter).zfill(3)

            all_agigs = self.gig_data.all_gigs_of_artist(a,True) # need to include future gigs here!
            artist_string = self.build_gigs_string( all_agigs, None, afname, None, a )

            breakdown = ''
            if len(c) > 1:
                unique_songs = self.gig_data.get_unique_songs_of_artist(a)

                events = [ x for x in c ]
                events.sort(key=lambda x: x.index)

                if len(c) > 3:
                    plot_fname = 'html/img/' + afname + '.png'
                    if self.plotter:
                        self.plotter.song_breakdown(a,events,unique_songs,plot_fname)
                    breakdown += '\n<br>\n<img class=png src="img/' + afname + '.png"><br>\n'
                    #plot_fname2 = 'html/img/' + afname + '_fd.png'
                    #if self.plotter:
                        #self.plotter.song_freq_dist(unique_songs,plot_fname2)
                    #breakdown += '\n<br>\n<img class=png src="img/' + afname + '_fd.png"><br>\n'
                # else:
                #     breakdown += '\n<br> \n' + '='*50

                breakdown += '<br><br>Breakdown of %d songs across %d events (%.2f songs/event):<br>' \
                                % ( len(unique_songs), len(c), len(unique_songs) / float(len(c)) )

                breakdown += '\n<table>'
                breakdown += '\n<br>'

                for song in unique_songs:
                    event_string = "<div class=breakdown>"
                    for event in events:
                        if event in song['events']:
                            symbol = 'X'
                            for s in event.sets:
                                if a in [x.name for x in s.artists]:
                                    for ss in s.songs:
                                        if ss.title == song['title']:
                                            if ss.solo:
                                                symbol = 'S'
                                            if s.solo and not ss.guests:
                                                symbol = 'S'
                                            if "partial" in ss.custom:
                                                symbol = 'P'
                                            break
                            title = song['title'] + ' / ' + event.venue + \
                                                    ' / ' + event.date.strftime("%d %b %Y")
                            link = event.link + '_' + afname + '.html'
                            event_string += '<a title="%s" href="%s">%s</a>' % (title, link, symbol)
                        else:
                            event_string += '-'
                    event_string += "</div>"
                    songtitle = song['title']
                    if song['obj'].cover:
                        #adding a hover title upsets the plain text alignment
                        symbol = '&curren;'
                        #symbol = '*'
                        cover_label = self.cover_artist_label(song['obj'].cover)
                        songtitle += ' <a href="covers.html#%s" title="%s">%s</a>' % \
                                            ( cover_label, song['obj'].cover + ' cover', symbol )
                    if song['obj'].improv:
                        songtitle += ' ' + self.make_flag_note('improv')

                    songcount = str(len(song['events']))
                    breakdown += self.row( [ songcount + self.sp(1), songtitle + self.sp(2), event_string ], 'rll' )
                    #breakdown += '<br>{0:3d} {1:50s} {2:30s}' \
                        #. format( len(song['events']), songtitle, event_string )
                breakdown += '\n</table>'

            breakdown += '\n<br>'
            self.make_file( afname, years_string_a, artist_string + breakdown, '' )

            for gig in c:
                suffix = '_a' + str(counter).zfill(3)
                link = gig.link + suffix
                artist_string_h = self.build_gigs_string( all_agigs, None, afname, None, a, gig.index )
                setlist_string = self.gig_setlist_string( gig, True, c, suffix)
                self.make_file( link, years_string_a, artist_string_h + breakdown, setlist_string, gig.img )

            link = '<a href=' + afname + '.html>' + a + '</a>'
            if self.gig_data.artist_is_support(a):
                link = '<i>' + link + '</i>'
            if len(c) == n_gigs_for_last_artist:
                artists_string += ', ' + link
            else:
                artists_string += '</td></tr>\n<tr><td align=right valign=top>' + str(len(c)) + \
                    '.' + self.sp(1) + '</td><td>' + link

            n_gigs_for_last_artist = len(c)

        artists_string += '\n</table>'
        
        return artists_string
    def make_venue_index_string(self,years_string_v):
        all_venues = self.gig_data.get_unique_venues()
        venues_string = str(len(self.gig_data.get_past_gigs())) + ' events at ' + \
                str(len(all_venues)) + ' venues:<br><br>\n<table>'
        n_gigs_for_last_venue = 0
        counter = 0
        for (v,c) in all_venues:
            counter += 1
            vfname = 'v' + str(counter).zfill(3)

            all_vgigs = self.gig_data.all_gigs_of_venue(v,True) # need to include future gigs here!
            venue_string = self.build_gigs_string( all_vgigs, None, vfname, v )

            vplot_link = ''
            # Plot venue growth:
            if len(c) > 3:
                plot_fname = 'html/img/' + vfname + '.png'
                if self.plotter:
                    self.plotter.general_plot(c, plot_fname, v)
                vplot_link = '<img src="img/%s.png">' % vfname

            self.make_file( vfname, years_string_v, venue_string, vplot_link )

            for gig in c:
                if gig.future:
                    break
                suffix = '_' + vfname
                link = gig.link + suffix
                venue_string_h = self.build_gigs_string( all_vgigs, None, vfname, v, None, gig.index )
                setlist_string = self.gig_setlist_string( gig, True, c, suffix)
                self.make_file( link, years_string_v, venue_string_h, setlist_string, gig.img )

            link = '<a href=' + vfname + '.html>' + v + '</a>'

            if len(c) == n_gigs_for_last_venue:
                venues_string += ', ' + link
            else:
                venues_string += '</td></tr>\n<tr><td align=right valign=top>' + str(len(c)) + \
                    '.' + self.sp(1) + '</td><td>' + link
            n_gigs_for_last_venue = len(c)

        venues_string += '</table>'

        cities = self.gig_data.unique_cities()
        n_cities = 0
        for (city,gigs_past,gigs_future) in cities:
            if len(gigs_past) > 0:
                n_cities += 1

        countries = self.gig_data.get_unique_countries()
        all_countries = list(countries.keys())
        all_countries.sort()

        venues_string += '\n<br>%d cities (in %d countries):<br><br>\n<table>' \
                % ( n_cities, len(all_countries) )

        n_gigs_for_last_city = 0
        counter = 0

        for (city,gigs_past,gigs_future) in cities:
            #print( "%s %d %d" % ( city, len(gigs_past), len(gigs_future) ) )
            #venues_string += '\n<tr><td align=right valign=top>' + str(len(c)) + '.' + self.sp(1) + \
                    #'</td><td>' + ', '.join([ x[0] for x in c]) + '</td></tr>'
            counter += 1
            cfname = 'c' + str(counter).zfill(3)
            clink = '<a href=' + cfname + '.html>' + city + '</a>' 

            all_cgigs = gigs_past + gigs_future;

            city_string = self.build_gigs_string( all_cgigs, None, cfname, city )

            cplot_link = ''
            # Plot city growth
            # if len(gigs_past) > 3:
            #     plot_fname = 'html/img/' + cfname + '.png'
            #     if self.plotter:
            #         self.plotter.general_plot(gigs_past+gigs_future,plot_fname,"City growth: " + city)
            #     cplot_link = '<img src="img/%s.png">' % cfname

            self.make_file( cfname, years_string_v, city_string, cplot_link )

            for gig in all_cgigs:
                suffix = '_' + cfname
                link = gig.link + suffix
                city_string_h = self.build_gigs_string( all_cgigs, None, cfname, city, None, gig.index )
                setlist_string = self.gig_setlist_string( gig, True, all_cgigs, suffix )
                self.make_file( link, years_string_v, city_string_h, setlist_string, gig.img )

            if len(gigs_past) == 0:
                pass
            elif len(gigs_past) == n_gigs_for_last_city:
                venues_string += ', ' + clink
            else:
                if n_gigs_for_last_city != None:
                    venues_string += '</td></tr>'

                venues_string += '\n<tr><td align=right valign=top>%d.%s</td><td>%s' \
                        % ( len(gigs_past), self.sp(1), clink )
            
            n_gigs_for_last_city = len(gigs_past)

        venues_string += '</td></tr></table>'

        # table of countries:
        # venues_string += "\n<br>%d countries:" % len(all_countries)
        # venues_string += '\n<ul>'
        # for country in all_countries:
        #     venues_string += "<li>%s (%d)" % (country, len(countries[country]))
        # venues_string += '</ul>'

        return venues_string
    def make_bootlegs_index_string(self):
        string = '\n<ul>'
        y = ""

        for g in self.gig_data.gigs:
            links = []
            for s in g.sets:
                if s.playlist:
                    link = '<a href="' + s.playlist + '">' + s.artists[0].name + '</a>'
                    links.append(link)
            if links:
                if y != g.date.strftime("%Y"):
                    string += '\n <br>'
                y = g.date.strftime("%Y")
                string += '\n  <br> <div class=date>%s</div> &nbsp;%s (%s)' % \
                            ( g.date.strftime("%Y-%b-%d"), " + ".join(links), g.venue )

        # for p in playlist_gigs:
        #     if y != p.date.strftime("%Y"):
        #         string += '\n <br>' # '========'
        #     y = p.date.strftime("%Y")
        #     links = []
        #     for s in p.sets:
        #         if s.playlist:
        #             link = '<a href="' + s.playlist + '">' + s.artists[0].name + '</a>'
        #             links.append(link)
        #     string += '\n  <br> <div class=date>' + p.date.strftime("%Y-%b-%d") + \
        #             '</div> &nbsp;' + " + ".join(links) + ' (' + p.venue + ')'

        string += '\n</ul>'
        return string
    def make_graphs_index_string(self):
        graphs = []

        if self.plotter:
            self.plotter.year_growth('html/img/plot_year_growth.png')
            self.plotter.total_progress('html/img/plot_cumulative.png')
            #self.plotter.month_growth('html/img/plot_month_growth.png')
            self.plotter.artist_growth('html/img/plot_artist_growth.png')
            self.plotter.venue_growth('html/img/plot_venue_growth.png')
            #self.plotter.relative_progress('html/img/plot_relative_progress.png')
            #self.plotter.days_growth('html/img/plot_days_growth.png')
            #self.plotter.top_venue_growth(9,'html/img/plot_top_venue_growth.png')
            self.plotter.h_index('html/img/plot_h_index.png')
            #self.plotter.freq_dist('html/img/plot_freq_dist.png')
            self.plotter.artist_demographics('html/img/plot_ages.png', \
                                     'html/img/plot_average_ages.png', \
                                     'html/img/plot_genders.png' )

        graphs.append('img/plot_year_growth.png')
        #graphs.append('img/plot_month_growth.png')
        graphs.append('img/plot_artist_growth.png')
        graphs.append('img/plot_venue_growth.png')
        graphs.append('img/plot_cumulative.png')
        #graphs.append('img/plot_relative_progress.png')
        #graphs.append('img/plot_days_growth.png')
        #graphs.append('img/plot_top_venue_growth.png')
        #graphs.append('img/plot_freq_dist.png')
        #graphs.append('img/plot_h_index.png')
        graphs.append('img/plot_ages.png')
        graphs.append('img/plot_genders.png')

        string = '<br> <br> <center>\n'
        count = 0

        for graph in graphs:
            count += 1
            string += '<img src="' + graph + '" style="width:30%;"><nbsp>'
            #if count % 2 == 0:
                #string += '<br>'
            string += '\n'

        string += '</center>\n'
        return string
    def make_calendar_string(self):
        # get future gigs
        cal_dates, cal_gigs = self.gig_data.calendar()

        lines = []

        month_days = [ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
        month_day_counts = []
        month_day_percentages = []

        for date, gigs in zip(cal_dates,cal_gigs):
            if date.day == 1:
                month_day_counts.append(0)
            if len(gigs) > 0:
                future = True
                for g in gigs:
                    if not g.future:
                        future = False
                if not future:
                    month_day_counts[-1] += 1

        total_coverage = 100 * sum(month_day_counts) / sum(month_days)
        total_fraction = "%d/%d" % ( sum(month_day_counts), sum(month_days) )
        #lines.append('Total coverage: %d days = %.2f%%' % (sum(month_day_counts), total_coverage ))
        #lines.append('<br><br>')

        for i, m in enumerate(month_day_counts):
            pc = 100 * month_day_counts[i] / month_days[i]
            month_day_percentages.append(pc)

        lines.append( '<table cellpadding=2>' )
        lines.append( '<tr>' )
        lines.append( '<td class="calendar_wide"><div title="%s">%.1f%%</div></td>' % \
                ( total_fraction, total_coverage ) )
        for day in range(1,32):
            lines.append( '<td align="center" class="calendar_wide">%s</td>' % day )
        lines.append( '</tr>' )

        for date, gigs in zip(cal_dates,cal_gigs):
            if date.day == 1:
                if date.month > 1:
                    lines.append('</tr>')
                lines.append('<tr>')
                m_index = int(date.strftime("%m")) - 1
                m_percent = month_day_percentages[m_index]
                div = '<div title="%.1f%% coverage">%s</div>' % ( m_percent, date.strftime("%B") )
                lines.append('<td class="calendar_wide">%s</td>' % div)
            if len(gigs) > 0:
                future = True
                links = []
                for i,g in enumerate(gigs):
                    year = str(g.date.year)
                    info = g.get_artists()[0] + ', ' + g.venue + ' (' + g.date.strftime('%A') + ')'
                    if not g.future:
                        link = '<a href=%s.html title="%s">%s</a>' % ( g.link, info, year )
                        links.append(link)
                        future = False
                    else:
                        link = '<div style="display: inline" title="%s">%s</div>' % ( info, year )
                        links.append(link)
                        # break # don't include multiple future gigs on a single date

                if future:
                    lines.append('<td class="calendar_empty">')
                else:
                    lines.append('<td class="calendar">')

                lines.append("<br>".join(links))
                lines.append('</td>')
            else:
                lines.append('<td class="calendar_empty">')
                lines.append('</td>')

        lines.append('</tr>')
        lines.append('</table>')

        return "\n".join(lines)
    def generate_html_files(self):
        self.make_stylesheet()

        extras = [ 'Artists', 'Venues' ]
        if self.do_playlists:
            extras += [ 'Tapes' ]
        if self.do_graphs:
            extras += [ 'Graphs' ]
        if self.do_covers_list:
            extras += [ 'Covers' ]
        if self.do_calendar:
            extras += [ 'Calendar' ]
        self.years = extras + [ '' ] + self.years

        years_string   = self.make_years_string()
        years_string_a = self.make_years_string("Artists")
        years_string_v = self.make_years_string("Venues")

        index_string   = ''
        years_string_i = ''
         
        for (y,c) in self.gig_data.get_unique_years(True):
            gigs_string = self.build_gigs_string(self.gig_data.gigs,y)
            years_string_h = self.make_years_string(y)

            plot_string = ''
            year_plot_path = 'img/plot_%s.jpg' % str(y)
            if self.plotter and self.plotter.total_progress_by_year('html/' + year_plot_path,y):
                plot_string += '<img class=yearplot src="%s">' % year_plot_path

            # Set the index page to the date of the next future gig:
            if y == self.gig_data.first_unseen().date.year:
                index_string = gigs_string
                years_string_i = years_string_h

            # It would be nice to display some stats on the current year:

            stats = self.gig_data.get_stats_by_year(y)

            if stats and stats["n_events"] > 0:
                n_events = stats["n_events"]
                n_new_dates = stats["n_new_dates"]
                n_artists = stats["n_artists"]
                n_new_artists = stats["n_new_artists"]
                n_headliners = stats["n_headliners"]
                n_new_headliners = stats["n_new_headliners"]
                n_male_headliners = stats["n_male_headliners"]
                n_female_headliners = stats["n_female_headliners"]
                n_venues = stats["n_venues"]
                n_new_venues = stats["n_new_venues"]
                n_cities = stats["n_cities"]
                n_new_cities = stats["n_new_cities"]
                n_countries = stats["n_countries"]
                n_new_countries = stats["n_new_countries"]

                year_stats =  "<br><ul>"
                year_stats += "<li> %d events (%d new dates)" % ( n_events, n_new_dates )
                year_stats += "<li> %d artists (%d new)" % ( n_artists, n_new_artists )
                year_stats += "<li> %d headliners (%d new) (%d male) (%d female)" % ( n_headliners, n_new_headliners, n_male_headliners, n_female_headliners )
                year_stats += "<li> %d venues (%d new)" % ( n_venues, n_new_venues )
                year_stats += "<li> %d cities (%d new)" % ( n_cities, n_new_cities )
                year_stats += "<li> %d countries (%d new)" % ( n_countries, n_new_countries )
                year_stats += "</ul>"
                plot_string += "<br>" + year_stats

            self.make_file( str(y), years_string_h, gigs_string, plot_string )
            for gig in self.gig_data.gigs:
                if gig.future:
                    continue
                if gig.date.year == y:
                    setlist_string = self.gig_setlist_string(gig)
                    gigs_string_h = self.build_gigs_string( self.gig_data.gigs, y, 
                                                            None, None, None, gig.index)
                    self.make_file( gig.link, 
                               years_string_h, gigs_string_h, setlist_string, gig.img)
            
        artists_string = self.make_artist_index_string(years_string_a)
        venues_string = self.make_venue_index_string(years_string_v)

        self.make_file( 'venues',    years_string_v,   venues_string,    '' )
        self.make_file( 'artists',   years_string_a,   artists_string,   '' )
        self.make_file( 'index',     years_string_i,   index_string,     '' )

        if self.do_playlists:
            years_string_b = self.make_years_string("Tapes")
            bootlegs_string = self.make_bootlegs_index_string()
            self.make_file( 'tapes',     years_string_b,   bootlegs_string,  '' )

        if self.do_graphs:
            years_string_g = self.make_years_string("Graphs")
            graphs_string = self.make_graphs_index_string()
            self.make_file( 'graphs',     years_string_g,   graphs_string,  '' )

        if self.do_covers_list:
            years_string_c = self.make_years_string("Covers")
            covers_string = self.make_covers_string()
            self.make_file( 'covers',    years_string_c,   covers_string,  '' )

        if self.do_calendar:
            years_string_c = self.make_years_string("Calendar")
            calendar_string = self.make_calendar_string()
            self.make_file( 'calendar', years_string_c, calendar_string, '' )

        return
    def make_covers_string(self):
        covers = self.gig_data.get_covers()
        string = '\n<ol>'
        for cover in covers:
            string += '<a name="%s"></a>' % self.cover_artist_label(cover['cover_artist'])
            string += '\n<li> <b>%s</b> (%d)' % ( cover['cover_artist'], cover['count'] )
            string += '\n    <ul>'
            songs = []
            for s, artists, gigs in zip( cover['songs'], cover['artists'], cover['gigs'] ):
                versions = []
                for a, g in zip(artists,gigs):
                    info = a + ', ' + g.venue
                    link = '<a href=%s.html title="%s">%s</a>' \
                            % ( g.link, info, g.date.strftime('%d-%b-%Y') )
                    versions.append( '%s' % link )
                    versions.sort()
                songs.append( '\n    <li> ' + s + ' (' + (', '.join(versions)) + ')' )
            songs.sort()
            string += ''.join(songs)
            string += '\n    </ul>'
            string += '\n    <br>'
        string += '\n</ol>'
        return string

