import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date

class GIG_plot():
    def __init__(self, gig_data):
        self.gig_data = gig_data
        self.n_graphs = 0
        self.colour1  = '#153E7E' # blue
        self.colour2  = '#C9BE62' # yellow
        self.colour3  = '#CCCCCC' # grey
        self.colour4  = '#8B0000' # red
        self.year     = gig_data.next_gig().date.year
    def top_venue_growth(self,top_n=5,dest=None):
        self.n_graphs += 1

        fig, ax = plt.subplots()
        venues = self.gig_data.get_unique_venues()[0:top_n]
        first_date = self.gig_data.get_unique_years()[0][1][0].date
        all_dates = [ first_date ]
        vnames = []
        for (v,gs) in venues:
            vnames.append(v)
            for g in gs:
                all_dates.append(g.date)

        all_dates.sort()

        for (v,gs) in venues:
            counts = []
            for d in all_dates:
                counts.append(0)

            for g in gs:
                indx = all_dates.index(g.date)
                for i in range(indx,len(all_dates)):
                    counts[i] += 1
            plt.plot(all_dates,counts,linewidth=2)

        ax.legend(vnames,loc='upper left')
        ax.set_xlim(datetime(all_dates[0].year-1,1,1),datetime(all_dates[-1].year+1,1,1))
        ax.set_ylim(0,len(venues[0][1])+1)

        years = [ x.year for x in all_dates ] 
        years = list(set(years))
        years.sort()
        years = list( range( years[0], years[-1]+1 ) )
        labels = [ str(x)[2:4] for x in years ]
        years = [ date(year=y, month=1, day=1) for y in years ]
        plt.xticks( years, labels )

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        #plt.title("Venue Growth (Top %d)" % top_n)
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def top_venues(self,top_n=5,dest=None):
        self.n_graphs += 1

        fig, ax = plt.subplots()
        venues = self.gig_data.get_unique_venues()[0:top_n]

        names = [ v[0] for v in venues ]
        counts = [ len(v[1]) for v in venues ]
        ind = list(range(len(counts)))

        bar1 = ax.bar( ind, counts, align='center', color=self.colour1 )

        plt.xticks(ind,names,rotation='vertical')

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        plt.title("Top Venues (Top %d)" % top_n)
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def artist_growth(self,dest=None,end_date=None):
        fig, ax = plt.subplots()

        self.n_graphs += 1

        y_gigs = self.gig_data.get_unique_years()
        y_gigs.sort()
        years = []
        n_artists = []
        n_new_artists = []
        all_artists = []
        n_new_headliners = []

        max_y_axis = 90

        for (y,c) in y_gigs:
            y_artists = []
            years.append(y)
            n_artists.append(0)
            n_new_artists.append(0)
            n_new_headliners.append(0)
            for g in c:
                if end_date and g.date > end_date:
                    continue
                set_index = 0
                for s in g.sets:
                    if s.artists[0].name in y_artists:
                        pass
                    else:
                        y_artists.append(s.artists[0].name)
                        n_artists[-1] += 1

                    if s.artists[0].name in all_artists:
                        pass
                    else:
                        all_artists.append(s.artists[0].name)
                        n_new_artists[-1] += 1
                        if set_index == 0:
                            n_new_headliners[-1] += 1
                    set_index += 1
        
        ind = range(1,len(years)+1)
        bar1 = ax.bar( ind, n_artists, align='center', \
                color=self.colour1, edgecolor=self.colour1 )
        bar2 = ax.bar( ind, n_new_artists, align='center', \
                       color=self.colour2, edgecolor=self.colour1 )
        bar3 = ax.bar( ind, n_new_headliners, align='center', \
                       color=self.colour3, edgecolor=self.colour1 )
        plt.xticks(ind,[str(xx)[2:4] for xx in years])

        if not end_date:
            plt.legend((bar1[0], bar2[0], bar3[0]), \
                       ('Total artists', 'New artists', 'New headliners'), \
                       loc='upper left')

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        #if end_date:
            #plt.ylim( [ 0, max_y_axis ] )

        plt.xlim( [0, len(years)+1] )

        #plt.title("Total artists seen per year")
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
    def month_growth(self,dest=None):
        self.n_graphs += 1
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month_totals = [0] * 12
        curr_totals = [0] * 12
        year_months = []

        for (y,c) in self.gig_data.get_unique_years():
            y_totals = [0] * 12
            for gig in c:
                i = int(gig.date.strftime("%m"))
                if gig.date.year == self.year:
                    curr_totals[i-1] += 1
                month_totals[i-1] += 1
                y_totals[i-1] += 1
            year_months.append(y_totals)

        month_maxima = []
        for x in range(0,12):
            month_maxima.append( max( [ y[x] for y in year_months ] ) )

        fig, ax = plt.subplots()
        ind = range(1,len(months)+1)

        bar1 = ax.bar( ind, month_totals,  align='center', \
                       color=self.colour1, edgecolor=self.colour1 )
        #bar2 = ax.bar( ind, month_maxima,  align='center', \
        #               color=self.colour3, edgecolor=self.colour1 )
        bar3 = ax.bar( ind, curr_totals,   align='center', \
                       color=self.colour2, edgecolor=self.colour1 )

        plt.xticks(ind,months)
        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim([0,len(ind)+1])
        # plt.legend( (bar1[0],bar3[0],bar2[0]), \
        #             ('Events in month', '%d events' % self.year, 'Month max'), \
        #             loc='upper left' )
        plt.legend( (bar1[0],bar3[0]), \
                    ('Events in month', '%d events' % self.year), \
                    loc='upper left' )

        #plt.title("Month histogram")
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
    def days_growth(self,dest=None):
        self.n_graphs += 1

        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        day_totals = [0] * 7
        curr_totals = [0] * 7
        for gig in self.gig_data.get_past_gigs():
            i = int(gig.date.strftime("%w"))
            if gig.date.year == self.year:
                curr_totals[i-1] += 1
            day_totals[i-1] += 1

        fig, ax = plt.subplots()
        ind = range(1,len(day_totals)+1)
        bar1 = ax.bar( ind, day_totals, align='center', color=self.colour1 )
        bar2 = ax.bar( ind, curr_totals, align='center', color=self.colour2 )
        plt.xticks(ind,days)
        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.legend( (bar1[0], bar2[0]), 
                    ('Events in day','%d events' % self.year), 
                    loc='upper left')
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
    def year_growth(self,dest=None,end_date=None):
        self.n_graphs += 1

        fig, ax = plt.subplots()
        y_gigs = self.gig_data.get_unique_years(True)
        y_gigs.sort()

        yday = datetime.today().timetuple().tm_yday
        if end_date:
            yday = end_date.timetuple().tm_yday
        years = []
        total_counts = []
        relative_counts = []
        dylan_counts = []
        future_counts = []  # total + future

        max_y_axis = 45

        for (y,c) in y_gigs:
            years.append(y)
            relative_counts.append(0)
            dylan_counts.append(0)
            total_counts.append(0)
            future_counts.append(0)
            for g in c:
                if end_date and g.date > end_date:
                    continue
                future_counts[-1] += 1

                if not g.future:
                    total_counts[-1] += 1
                    if g.date.timetuple().tm_yday <= yday:
                        relative_counts[-1] += 1
                    if 'Bob Dylan' in g.get_artists():
                        dylan_counts[-1] += 1

            if y == self.year:
                break

        plot_up_to_day = True
        if total_counts[-1] == 0 and total_counts[-2] == future_counts[-2]:
            plot_up_to_day = False
        elif total_counts[-1] == future_counts[-1]:
            plot_up_to_day = False

        ind = range(1,len(years)+1)
        if not end_date:
            bar_future = ax.bar( ind, future_counts, align='center', \
                                 color=self.colour3, edgecolor=self.colour1 )
        bar_tot = ax.bar( ind, total_counts, align='center', \
                          color=self.colour1, edgecolor=self.colour1 )

        if plot_up_to_day:
            bar_rel = ax.bar( ind, relative_counts, align='center', \
                              color=self.colour2, edgecolor=self.colour1 )

        #bar_dyl = ax.bar( ind, dylan_counts,    0.4,  align='center', \
        #                  color=self.colour4, edgecolor=self.colour1 )

        plt.xticks(ind,[str(xx)[2:4] for xx in years])

        today = datetime.today()
        ordinal = lambda n: str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
        datestr = str(ordinal(today.day)) + today.strftime(" %b")
        plt.legend((bar_tot[0],), ('Up to %s' % datestr,), loc='upper left')

        if not end_date:
            data = (bar_tot[0], 
                   #bar_rel[0], 
                   #bar_dyl[0], 
                    bar_future[0])

            keys = ('Total events',
                   #'Up to %s' % datestr,
                   #'Dylan events',
                    'Planned events')

            if plot_up_to_day:
                data = (bar_tot[0], 
                        bar_rel[0], 
                       #bar_dyl[0], 
                        bar_future[0])

                keys = ('Total events',
                        'Up to %s' % datestr,
                       #'Dylan events',
                        'Planned events')

            plt.legend(data, keys, loc='upper left' )

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        if end_date:
            plt.ylim( [ 0, max_y_axis ] )

        plt.xlim( [0, len(years)+1] )

        #plt.title("Year Histogram")
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
    def venue_growth(self,dest=None,end_date=None):
        fig, ax = plt.subplots()

        self.n_graphs += 1

        y_gigs = self.gig_data.get_unique_years()
        y_gigs.sort()
        years = []
        n_venues = []
        n_new_venues = []
        all_venues = []
        all_cities = []
        n_new_cities = []

        max_y_axis = 30

        for (y,c) in y_gigs:
            y_venues = []
            years.append(y)
            n_venues.append(0)
            n_new_venues.append(0)
            n_new_cities.append(0)
            for g in c:
                if end_date and g.date > end_date:
                    continue
                if g.venue in y_venues:
                    pass
                else:
                    y_venues.append(g.venue)
                    n_venues[-1] += 1
                    if g.city in all_cities:
                        pass
                    else:
                        all_cities.append(g.city)
                        n_new_cities[-1] += 1

                if g.venue in all_venues:
                    pass
                else:
                    all_venues.append(g.venue)
                    n_new_venues[-1] += 1

        ind = range(1,len(years)+1)
        bar1 = ax.bar( ind, n_venues, align='center', \
                       color=self.colour1, edgecolor=self.colour1 )
        bar2 = ax.bar( ind, n_new_venues, align='center', \
                       color=self.colour2, edgecolor=self.colour1 )
        bar3 = ax.bar( ind, n_new_cities, align='center', \
                       color=self.colour3, edgecolor=self.colour1 )
        plt.xticks(ind,[str(xx)[2:4] for xx in years])
        if end_date:
            plt.ylim( [ 0, max_y_axis ] )

        if not end_date:
            plt.legend((bar1[0], bar2[0], bar3[0]), \
                       ('Total venues', 'New venues', 'New cities'), \
                       loc='upper left')

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        plt.xlim( [0, len(years)+1] )

        #plt.title("Total venues seen per year")
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
    def h_index(self,dest=None):
        gigs = self.gig_data.gigs[:]

        h_dates = []
        h_values = []
        f_h_dates = []
        f_h_values = []

        artist_counts = {}

        for gig in gigs:
            for a in gig.get_artists():
                if a in artist_counts:
                    artist_counts[a] += 1
                else:
                    artist_counts[a] = 1

            l = list(artist_counts.items())
            l.sort(key=lambda x: x[1])
            l.reverse()

            # calculate h for this subset
            current_h = 0
            for i, (a, c) in enumerate(l):
                if c >= i+1:
                    current_h = i+1
                else:
                    break

            if len(h_values) == 0 or current_h != h_values[-1]:

                if gig.future:
                    if len(f_h_values) == 0:
                        f_h_values.append(h_values[-1])
                        f_h_dates.append(h_dates[-1])
                    f_h_values.append(current_h)
                    f_h_dates.append(gig.date)
                else:
                    h_values.append(current_h)
                    h_dates.append(gig.date)

        self.n_graphs += 1

        fig, ax = plt.subplots()

        line1 = plt.plot(h_dates,h_values,color=self.colour1) #,linewidth=2.0)
        line2 = plt.plot(f_h_dates,f_h_values,color=self.colour1,ls='--') #,linewidth=2.0)
        dots1 = plt.plot(h_dates,h_values,color=self.colour2,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)

        years = [ date(y[0],1,1) for y in self.gig_data.get_unique_years() ]
        plt.xticks(years,[xx.strftime("%y") for xx in years])

        plt.legend((line1[0],line2[0]), ('Artist h-index','Planned'), loc='upper left')

        ax.set_axisbelow(True)

        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim([datetime.strptime(str(years[0].year-1),"%Y"),
                  datetime.strptime(str(years[-1].year+1),"%Y")])

        plt.ylim( bottom=0, top=10 )

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def freq_dist(self,dest=None):
        self.n_graphs += 1

        fig, ax = plt.subplots()
        a_gigs = self.gig_data.get_unique_artists()

        freq = [ 0 ] * len(a_gigs[0][1] )

        for (a,c) in a_gigs:
            freq[ len(c) - 1 ] += 1

        ind = range(1,len(freq)+1)
        bar1 = ax.bar( ind, freq, align='center', color=self.colour1 )
        plt.xticks(ind, [ str(i+1) if freq[i] > 0 else "" for i in range(0,len(freq)) ] )
        plt.legend((bar1[0],), ('Artist frequency distribution',), loc='upper right')
        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        #plt.title("Frequency Distribution of Artists")
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def relative_progress(self,dest=None):
        self.n_graphs += 1

        yday = datetime.today().timetuple().tm_yday

        gig_counts = []
        gig_years = []

        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()

        for (y,c) in gigs_by_year:
            gig_years.append(y)
            gig_counts.append(0)
            for g in c:
                if g.date.timetuple().tm_yday <= yday:
                    gig_counts[-1] += 1
            
        #print( "gig_counts: %s" % ",".join( str(x) for x in gig_counts ) )

        fig, ax = plt.subplots()

        ind = range(1,len(gig_counts)+1)
        bar1 = ax.bar( ind, gig_counts, align='center', \
                       color=self.colour1, edgecolor=self.colour1 )
        plt.xticks(ind, [str(xx)[2:4] for xx in gig_years] )

        today = datetime.today()
        ordinal = lambda n: str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
        datestr = str(ordinal(today.day)) + today.strftime(" %b")
        plt.legend((bar1[0],), ('Up to %s' % datestr,), loc='upper left')

        #plt.title("Relative Progress")
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)
        plt.ylim([0,max(gig_counts)+1])
        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def total_progress(self,dest=None,end_date=None):
        self.n_graphs += 1

        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()

        running_total = 0
        totals = []
        dates = []
        years = []

        max_y_axis = 450

        for (y,c) in gigs_by_year:
            # running_total += 1 # comment this out for cumulative annual count
            years.append(datetime.strptime(str(y),"%Y"))
            for g in c:
                if end_date and g.date > end_date:
                    continue
                running_total += 1
                totals.append(running_total)
                dates.append(g.date)
            
        #print( "gig_counts: %s" % ",".join( str(x) for x in gig_counts ) )
        fig, ax = plt.subplots()

        line1 = plt.plot(dates,totals,color=self.colour1) #,linewidth=2.0)
        plt.xticks(years,[xx.strftime("%y") for xx in years])

        if not end_date:
            plt.legend((line1[0],), ('Cumulative event count',), loc='upper left')

        ax.set_axisbelow(True)
        ax.fill_between(dates, 0, totals, color=self.colour1)

        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim([datetime.strptime(str(years[0].year-1),"%Y"),
                  datetime.strptime(str(years[-1].year+1),"%Y")])

        plt.ylim( bottom=0 )

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def total_progress_by_year(self,dest,year):
        gigs = None

        for (y,c) in self.gig_data.get_unique_years(True):
            if y == year:
                gigs = c

        running_total = 0
        totals = []
        dates = []
        bob_totals = []
        bob_dates = []
        future_dates = []
        future_totals = []
        
        if gigs == None:
            return False

        for g in gigs:
            running_total += 1
            if g.future:
                future_dates.append(g.date)
                future_totals.append(running_total)
            else:
                if 'Bob Dylan' in g.get_artists():
                    bob_totals.append(running_total)
                    bob_dates.append(g.date)
                totals.append(running_total)
                dates.append(g.date)
                future_dates = [ g.date ]
                future_totals = [ running_total ]

        months = [ date(year=year, month=x, day=1) for x in range(1,13) ]

        fig, ax = plt.subplots()

        blobs = dates[:]
        blob_totals = totals[:]

        # if len(future_dates) > 1:
        #     future_dates.append( date(year=year, month=12, day=31) )
        #     future_totals.append( future_totals[-1] )

        #dates.insert(0, date(year=year, month=1, day=1) )
        #totals.insert(0,0)
        line1 = None

        if len(dates) > 1:
            line1 = plt.plot(dates,totals,color=self.colour1) #,linewidth=2.0)

        if len(future_dates) > 1:
            line2 = plt.plot(future_dates,future_totals,color=self.colour1,ls='--')

        dots1 = plt.plot(blobs,blob_totals,color=self.colour2,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)
        dots2 = plt.plot(bob_dates,bob_totals,color=self.colour4,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)

        plt.xticks(months, [x.strftime(" %b") for x in months], ha='left')
        if running_total <= 10:
            plt.yticks(range(0,50,5))

        ax.set_axisbelow(True)

        # if len(future_dates) > 1:
        #     pass
        #     #dates.append( datetime.today() )
        #     #totals.append( totals[-1] )
        # else:
        #     dates.append( date(year=year, month=12, day=31) )
        #     totals.append( totals[-1] )

        ax.fill_between(dates, 0, totals, color=self.colour1)

        if len(dates) > 1 and len(future_dates) > 1 and line1:
            plt.legend( (line1[0],line2[0]), 
                        ('%d events' % year, 'Planned'), 
                        loc='upper left')
        elif len(dates) > 1 and line1:
            plt.legend((line1[0],), ('%d events' % year,), loc='upper left')
        elif len(future_dates) > 1:
            plt.legend((line2[0],), ('%d planned' % year,), loc='upper left')

        max_y_axis = 45
        plt.xlim([ date(year=year, month=1, day=1), date(year=year, month=12, day=31) ])
        plt.ylim([0,max_y_axis])
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        # # for current year, draw straight line from 0 to 40 gigs:
        # if year == datetime.today().year:
        #     xs = [ date(year, 1, 1), date(year, 12, 31) ]
        #     ys = [ 0, 40 ]
        #     plt.plot(xs, ys, zorder=-10, color="green", linewidth=0.5)

        fig.savefig(dest, bbox_inches='tight')
        plt.close()

        return True
    def song_breakdown(self,artist,events,unique_songs,dest=None):
        event_idx = list(range(1,len(events)+1))
        new_songs = [0] * len(events)
        support_new_songs = []
        support_dates = []
        
        for song in unique_songs:
            index = 0
            for event in events:
                if event in song['events']:
                    new_songs[index] += 1
                    break
                index += 1

        for i in range(1,len(events)):
            new_songs[i] += new_songs[i-1]

        for i in range(0,len(events)):
            if events[i].get_artists()[0] != artist:
                support_new_songs.append(new_songs[i])
                support_dates.append(events[i].date.date())

        #print(event_idx)
        #print(new_songs)

        fig, ax = plt.subplots()
        ax.set_axisbelow(True)
        ax.margins(0.05)

        #line1 = plt.plot(event_idx,new_songs,marker='.')

        # plotting against date rather than index breaks something in plt:
        dates = [e.date.date() for e in events]
        line1 = plt.plot(dates,new_songs)
        dots1 = plt.plot(dates,new_songs,color=self.colour2,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)
        dots2 = plt.plot(support_dates,support_new_songs,color=self.colour1,marker='o',ls='')

        plt.legend((line1[0],), ('Unique song count: ' + artist,), loc='upper left')

        # Ensure a tick for each year:
        final_year = dates[-1].year + 1
        years = list( range( dates[0].year, final_year+1 ) )
        years = [ date( year=x, month=1, day=1 ) for x in years ]
        plt.xticks(years, [ str(x.year)[2:4] for x in years ] )

        plt.grid(b=True, which='both')

        if dest:
            fig.savefig( dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def song_freq_dist(self,unique_songs,dest=None):
        counts = [ len(s['events']) for s in unique_songs ]
        max_count = max(counts)

        fig, ax = plt.subplots()
        ax.set_axisbelow(True)
        
        index = []
        f_dist = []
        for x in range(1,max_count+1):
            index.append(x)
            f_dist.append( counts.count(x) )

        bar1 = ax.bar( index, f_dist, align='center', color=self.colour1 )
        plt.xticks(index)

        if len(index) > 10:
            for label in ax.xaxis.get_ticklabels()[::2]:
                label.set_visible(False)

        plt.legend( (bar1[0],), ('Freq dist',), loc='upper right' )
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        fig.canvas.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
    def activity(self,dest=None):
        dates = [ x.date for x in self.gig_data.get_past_gigs() ]
        dates.sort()

        which = 'weeks'
        which = 'months'
        which = 'days'
        which = 'years'

        divisions = []
        gigcounts = []

        if which == 'days':
            cur_day = dates[0]
            last_day = dates[-1]

            divisions = []
            while cur_day <= last_day:
                divisions.append(cur_day)
                cur_day += timedelta(days=1)

            gigcounts = [0] * len(divisions)
            for d in dates:
                pos = divisions.index(d)
                gigcounts[pos] += 1
        elif which == 'weeks':
            weekstart = lambda d: d - timedelta(days=d.weekday())

            one_week = timedelta(days=7)
            cur_week = weekstart(dates[0])
            last_week  = weekstart(dates[-1])

            divisions = []
            while cur_week <= last_week:
                divisions.append(cur_week)
                cur_week += one_week

            gigcounts = [0] * len(divisions)
            for d in dates:
                pos = divisions.index(weekstart(d))
                gigcounts[pos] += 1
        elif which == 'months':
            monthstart = lambda d: date( year=d.year, month=d.month, day=1 )
            addmonth = lambda d: date( year = int(d.year + d.month / 12 ),
                                       month = d.month % 12 + 1, day = 1 )

            cur_month = monthstart(dates[0])
            last_month = monthstart(dates[-1])

            divisions = []
            while cur_month <= last_month:
                divisions.append(cur_month)
                cur_month = addmonth(cur_month)
            
            gigcounts = [0] * len(divisions)
            for d in dates:
                pos = divisions.index(monthstart(d))
                gigcounts[pos] += 1
        elif which == 'years':
            cur_year = dates[0].year
            last_year = dates[-1].year

            divisions = []
            while cur_year <= last_year:
                divisions.append(cur_year)
                cur_year += 1

            gigcounts = [0] * len(divisions)
            for d in dates:
                pos = divisions.index(d.year)
                gigcounts[pos] += 1
            
        fig, ax = plt.subplots()
        #bar1 = ax.bar(divisions, gigcounts, align='center', color=self.colour1 )
        line1 = plt.plot(divisions, gigcounts, color=self.colour1)
        ax.fill_between(divisions, 0, gigcounts, color=self.colour1)

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both')

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def general_plot(self,gigs,dest,title):
        self.n_graphs += 1

        dates_future = []
        totals_future = []
        dates = []
        totals = []

        for gig in gigs:
            if gig.future:
                dates_future.append(gig.date)
                if len(totals_future) == 0:
                    totals_future.append(1)
                else:
                    totals_future.append( totals_future[-1] + 1 )
            else:
                dates.append(gig.date)
                if len(totals) == 0:
                    totals.append(1)
                else:
                    totals.append( totals[-1] + 1 )

        dates_future.insert( 0, dates[-1] )
        totals_future.insert( 0, 0 )
        totals_future = [ (x + totals[-1]) for x in totals_future ]

        years = []
        if dates_future:
            years = range( dates[0].year, dates_future[-1].year +2 )
        else:
            years = range( dates[0].year, dates[-1].year +2 )
        years = list(set(list(years)))
        years.sort()
        years = [ date(year=y,month=1,day=1) for y in years ]


        fig, ax = plt.subplots()

        line1 = plt.plot(dates,totals,color=self.colour1) #,linewidth=2.0)
        line2 = plt.plot(dates_future,totals_future,color=self.colour1,ls='--')
        dots1 = plt.plot(dates,totals,color=self.colour2,marker='o',ls='',\
                         markeredgewidth=1,markeredgecolor=self.colour1)

        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.legend((line1[0],), (title,), loc='upper left')
        plt.xticks(years,[str(y.year)[2:] for y in years])

        ax.fill_between(dates, 0, totals, color=self.colour1)

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim([years[0], years[-1]])

        plt.ylim( bottom=0 )

        if dest:
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def artist_demographics(self,dest_ages=None,dest_av=None,dest_genders=None):
        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()

        ages = {}
        ages_bob = {}
        average_ages = {}
        genders = {}

        for (y,c) in gigs_by_year:
            total_age = 0    
            n_artists = 0
            gender_totals = [0,0]
            for g in c:
                date = g.date.date()
                artist = g.sets[0].artists[0]
                age = artist.age(date)
                gender = artist.gender()

                if age:
                    total_age += age
                    n_artists += 1
                    #print("%s (%d)" % (artist.name, age))
                    age = str(age)
                    if not age in ages:
                        ages[age] = 0
                    ages[age] += 1

                    if artist.name == "Bob Dylan":
                        if not age in ages_bob:
                            ages_bob[age] = 0
                        ages_bob[age] += 1
                if gender:
                    if gender == 'male':
                        gender_totals[0] += 1
                    elif gender == 'female':
                        gender_totals[1] += 1
                    
            if n_artists > 0:
                average_ages[str(y)] = total_age / n_artists
                genders[str(y)] = gender_totals
            else:
                average_ages[str(y)] = 0
                genders[str(y)] = [0,0]

        #print(ages)
        #print(ages_bob)
        #print(average_ages)
        #print(genders)

        if ages and ages_bob:
            alist = [ int(a) for a in ages.keys() ]
            alist.sort()
            
            graph_ages = list(range(min(alist),max(alist)+1))

            graph_freq = []
            graph_freq_bob = []

            for age in graph_ages:
                if str(age) in ages:
                    graph_freq.append(ages[str(age)])
                else:
                    graph_freq.append(0)

                if str(age) in ages_bob:
                    graph_freq_bob.append(ages_bob[str(age)])
                else:
                    graph_freq_bob.append(0)

            fig, ax = plt.subplots()
            ax.set_axisbelow(True)
            bar1 = ax.bar(graph_ages, graph_freq, width=1, align='center', \
                          color=self.colour1, edgecolor=self.colour1)
            bar2 = ax.bar(graph_ages, graph_freq_bob, width=1, align='center', \
                          color=self.colour2, edgecolor=self.colour1)
            plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

            plt.legend( (bar1[0],bar2[0]), \
                        ('Ages of headliners', 'Ages of Bob Dylan'), \
                        loc='upper left' )

            if dest_ages:
                fig.savefig(dest_ages, bbox_inches='tight')
                plt.close()
            else:
                plt.show(block=False)
                plt.show()

        if average_ages:
            yr_list = [ int(a) for a in average_ages.keys() ]
            yr_list.sort()

            av_ages = []

            for y in yr_list:
                if str(y) in average_ages.keys():
                    av_ages.append( average_ages[ str(y) ] )
                else:
                    av_ages.append( 0 )

            #print(yr_list)
            #print(av_ages)

            fig, ax = plt.subplots()
            ax.set_axisbelow(True)
            line1 = plt.plot(yr_list, av_ages, color=self.colour1)
            plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
            plt.xticks(yr_list,[str(xx)[2:] for xx in yr_list])

            #plt.legend( (bar2[0],bar1[0]), \
                        #('Ages of headliners', 'Ages of Bob Dylan'), \
                        #loc='upper left' )

            if dest_av:
                fig.savefig(dest_av, bbox_inches='tight')
                plt.close()
            else:
                plt.show(block=False)
                plt.show()

        if genders:
            yr_list = [ int(a) for a in genders.keys() ]
            yr_list.sort()

            n_male = []
            n_female = []

            for y in yr_list:
                if str(y) in genders.keys():
                    n_male.append(   genders[ str(y) ][0] )
                    n_female.append( genders[ str(y) ][1] )
                else:
                    n_male.append(   0 )
                    n_female.append( 0 )

            width = 0.35
            fig, ax = plt.subplots()
            ax.set_axisbelow(True)
            bar1 = plt.bar([y-width/2 for y in yr_list], n_male,   width, color=self.colour1)
            bar2 = plt.bar([y+width/2 for y in yr_list], n_female, width, color=self.colour2, \
                           edgecolor=self.colour1)
            plt.xticks(yr_list,[str(xx)[2:] for xx in yr_list])
            plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

            plt.legend( (bar1[0],bar2[0]), \
                        ('Male headliners', 'Female headliners'), \
                        loc='upper left' )

            if dest_genders:
                fig.savefig(dest_genders, bbox_inches='tight')
                plt.close()
            else:
                plt.show(block=False)
                plt.show()
            

