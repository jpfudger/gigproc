import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta, date

class GIG_plot():
    def __init__(self, gig_data):
        self.gig_data = gig_data
        self.n_graphs = 0
        self.graph_size = (6.5, 4.5)
        self.colour1  = '#153E7E' # blue
        self.colour2  = '#C9BE62' # yellow
        self.colour3  = '#CCCCCC' # grey
        self.colour4  = '#8B0000' # red
        self.year     = gig_data.next_gig().date.year
        self.stats    = gig_data.get_stats_by_year()
    def top_venues(self,top_n=5,dest=None):
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
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def top_artists(self,top_n=5,dest=None):
        self.n_graphs += 1

        fig, ax = plt.subplots()
        artists = self.gig_data.get_unique_artists()[0:top_n]
        first_date = self.gig_data.get_unique_years()[0][1][0].date
        all_dates = [ first_date ]
        anames = []
        for (a,gs) in artists:
            anames.append(a)
            for g in gs:
                all_dates.append(g.date)

        all_dates.sort()

        for (a,gs) in artists:
            counts = []
            for d in all_dates:
                counts.append(0)

            for g in gs:
                indx = all_dates.index(g.date)
                for i in range(indx,len(all_dates)):
                    counts[i] += 1

            plt.plot(all_dates,counts,linewidth=2)

        ax.legend(anames,loc='upper left')
        ax.set_xlim(datetime(all_dates[0].year-1,1,1),datetime(all_dates[-1].year+1,1,1))
        ax.set_ylim(0,len(artists[0][1])+1)

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
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def artists_by_year(self,dest=None):
        fig, ax = plt.subplots()
        self.n_graphs += 1

        years            = [ d["year"]                  for d in self.stats if d["n_events"] > 0]
        n_artists        = [ len(d["n_artists"])        for d in self.stats if d["n_events"] > 0]
        n_new_artists    = [ len(d["n_new_artists"])    for d in self.stats if d["n_events"] > 0]
        n_new_headliners = [ len(d["n_new_headliners"]) for d in self.stats if d["n_events"] > 0]

        ind = range(1,len(years)+1)
        bar1 = ax.bar( ind, n_artists, align='center', \
                color=self.colour1, edgecolor=self.colour1 )
        bar2 = ax.bar( ind, n_new_artists, align='center', \
                       color=self.colour2, edgecolor=self.colour1 )
        bar3 = ax.bar( ind, n_new_headliners, align='center', \
                       color=self.colour3, edgecolor=self.colour1 )
        plt.xticks(ind,[str(xx)[2:4] for xx in years])

        plt.legend((bar1[0], bar2[0], bar3[0]), \
                   ('Total artists', 'New artists', 'New headliners'), \
                   loc='upper left')

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim( [0, len(years)+1] )

        #plt.title("Total artists seen per year")
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
    def percentage_new_artists_by_year(self,dest=None):
        fig, ax = plt.subplots()
        self.n_graphs += 1

        years            = [ d["year"]                  for d in self.stats if d["n_events"] > 0]
        n_artists        = [ len(d["n_artists"])        for d in self.stats if d["n_events"] > 0]
        n_new_artists    = [ len(d["n_new_artists"])    for d in self.stats if d["n_events"] > 0]
        n_headliners     = [ len(d["n_headliners"])     for d in self.stats if d["n_events"] > 0]
        n_new_headliners = [ len(d["n_new_headliners"]) for d in self.stats if d["n_events"] > 0]

        perc_new_artists = []
        perc_new_headliners = []

        for n, n_new in zip(n_artists, n_new_artists):
            perc_new_artists.append(100 * n_new / n)

        for n, n_new in zip(n_headliners, n_new_headliners):
            perc_new_headliners.append(100 * n_new / n)

        ind = range(1,len(years)+1)
        bar1 = ax.bar( ind, perc_new_artists, align='center', \
                color=self.colour1, edgecolor=self.colour1 )
        bar2 = ax.bar( ind, perc_new_headliners, align='center', \
                       color=self.colour2, edgecolor=self.colour1 )
        plt.xticks(ind,[str(xx)[2:4] for xx in years])

        plt.legend((bar1[0], bar2[0]), \
                   ('% new artists', '% new headliners'), \
                   loc='upper right')

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim( [0, len(years)+1] )

        #plt.title("Total artists seen per year")
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
    def events_by_day_and_month(self,dest=None):
        self.n_graphs += 1

        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

        day_totals = [0] * 7
        days_current = [0] * 7

        month_totals = [0] * 12
        months_current = [0] * 12

        for gig in self.gig_data.get_past_gigs():
            day_i = int(gig.date.strftime("%w"))
            month_i = int(gig.date.strftime("%m"))

            if gig.date.year == self.year:
                days_current[day_i-1] += 1
                months_current[month_i-1] += 1

            day_totals[day_i-1] += 1
            month_totals[month_i-1] += 1

        bars = months + [''] + days
        #bars = [ x[0] if x else "" for x in bars ] # first letters, to save space
        data_total = month_totals + [0] + day_totals
        data_current = months_current + [0] + days_current

        fig, ax = plt.subplots()
        ind = range(1,len(data_total)+1)
        bar1 = ax.bar( ind, data_total,   align='center', color=self.colour1 )
        bar2 = ax.bar( ind, data_current, align='center', color=self.colour2 )

        plt.xticks(ind,bars)
        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        plt.xlim([0,len(ind)+1])

        legend_bars = (bar1[0], bar2[0],)
        legend_text = ('Events by day/month','%d events' % self.year,) 

        if sum(data_current) == 0:
            legend_bars = (bar1[0], )
            legend_text = ('Events by day/month', )

        plt.legend(legend_bars, legend_text, loc='upper left')
        #fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
    def events_by_year(self,dest=None,end_date=None):
        self.n_graphs += 1
        fig, ax = plt.subplots()

        years            = [ d["year"]          for d in self.stats if d["n_events"] > 0]
        total_counts     = [ d["n_events"]      for d in self.stats if d["n_events"] > 0]
        relative_counts  = [ d["n_relative"]    for d in self.stats if d["n_events"] > 0]
        dylan_counts     = [ d["n_dylan"]       for d in self.stats if d["n_events"] > 0]
        future_counts    = [ d["n_future"]      for d in self.stats if d["n_events"] > 0]
        ticket_counts    = [ d["n_future_confirmed"] for d in self.stats if d["n_events"] > 0]

        for i, year in enumerate(years):
            if future_counts[i] > 0:
                future_counts[i] += total_counts[i]
            if ticket_counts[i] > 0:
                ticket_counts[i] += total_counts[i]

        plot_up_to_day = future_counts[-1] > 0
        plot_future = (future_counts[-1] > 0) and (not end_date)
        if sum(relative_counts[:-1]) == 0:
            plot_up_to_day = False

        ind = range(1,len(years)+1)

        if plot_future:
            # plot future first, so that totals go in front
            bar_future = ax.bar( ind, ticket_counts, align='center', \
                                 color=self.colour3, edgecolor=self.colour1 )

            # bar_ticket = ax.bar( ind, ticket_counts, align='center', \
            #                  color=self.colour5, edgecolor=self.colour1 )

        bar_tot = ax.bar( ind, total_counts, align='center', \
                          color=self.colour1, edgecolor=self.colour1 )

        if plot_up_to_day:
            relative_counts[-1] = 0
            bar_rel = ax.bar( ind, relative_counts, align='center', \
                              color=self.colour2, edgecolor=self.colour1 )

        bar_dyl = ax.bar( ind, dylan_counts,    0.4,  align='center', \
                          color=self.colour4, edgecolor=self.colour1 )

        plt.xticks(ind,[str(xx)[2:4] for xx in years])

        today = datetime.today()
        ordinal = lambda n: str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
        datestr = str(ordinal(today.day)) + today.strftime(" %b")

        if plot_up_to_day and plot_future:
            #print("UP TO DAY")
            data = [bar_tot[0], 
                    bar_rel[0], 
                    bar_dyl[0],
                    bar_future[0],
                    #bar_ticket[0],
                    ]

            keys = ['Total events',
                    'Past years up to %s' % datestr,
                    'Dylan events',
                    'Planned events',
                    #'Confirmed events',
                    ]
        elif plot_future:
            #print("GOT FUTURE")
            data = [bar_tot[0], 
                    bar_dyl[0],
                    bar_future[0],
                    #bar_ticket[0],
                    ]

            keys = ['Total events',
                    'Dylan events',
                    'Planned events',
                    #'Confirmed events',
                    ]
        else:
            #print("GOT NO FUTURE")
            data = [bar_tot[0],
                    bar_dyl[0]]

            keys = ['Total events',
                    'Dylan events']

        plt.legend(data, keys, loc='upper left' )
        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim( [0, len(years)+1] )

        #plt.title("Year Histogram")
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
    def venues_by_year(self,dest=None):
        fig, ax = plt.subplots()
        self.n_graphs += 1
 
        years        = [ d["year"]              for d in self.stats if d["n_events"] > 0]
        n_venues     = [ len(d["n_venues"])     for d in self.stats if d["n_events"] > 0]
        n_new_venues = [ len(d["n_new_venues"]) for d in self.stats if d["n_events"] > 0]
        n_new_cities = [ len(d["n_new_cities"]) for d in self.stats if d["n_events"] > 0]

        ind = range(1,len(years)+1)
        bar1 = ax.bar( ind, n_venues, align='center', \
                       color=self.colour1, edgecolor=self.colour1 )
        bar2 = ax.bar( ind, n_new_venues, align='center', \
                       color=self.colour2, edgecolor=self.colour1 )
        bar3 = ax.bar( ind, n_new_cities, align='center', \
                       color=self.colour3, edgecolor=self.colour1 )
        plt.xticks(ind,[str(xx)[2:4] for xx in years])

        plt.legend((bar1[0], bar2[0], bar3[0]), \
                   ('Total venues', 'New venues', 'New towns'), \
                   loc='upper left')

        ax.set_axisbelow(True)
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        plt.xlim( [0, len(years)+1] )

        #plt.title("Total venues seen per year")
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
    def h_index(self,dest=None):
        gigs = self.gig_data.gigs[:]

        artist_counts = {}
        artist_h_dates = []
        artist_h_values = []
        artist_f_h_dates = []
        artist_f_h_values = []

        venue_counts = {}
        venue_h_dates = []
        venue_h_values = []
        venue_f_h_dates = []
        venue_f_h_values = []

        for gig in gigs:
            # ARTIST CALCULATION

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

            if len(artist_h_values) == 0 or current_h != artist_h_values[-1]:

                if gig.future:
                    if len(artist_f_h_values) == 0:
                        artist_f_h_values.append(artist_h_values[-1])
                        artist_f_h_dates.append(artist_h_dates[-1])
                    artist_f_h_values.append(current_h)
                    artist_f_h_dates.append(gig.date)
                else:
                    artist_h_values.append(current_h)
                    artist_h_dates.append(gig.date)

            # VENUE CALCULATION

            if gig.venue in venue_counts:
                venue_counts[gig.venue] += 1
            else:
                venue_counts[gig.venue] = 1

            l = list(venue_counts.items())
            l.sort(key=lambda x: x[1])
            l.reverse()

            # calculate h for this subset
            current_h = 0
            for i, (a, c) in enumerate(l):
                if c >= i+1:
                    current_h = i+1
                else:
                    break

            if len(venue_h_values) == 0 or current_h != venue_h_values[-1]:

                if gig.future:
                    if len(venue_f_h_values) == 0:
                        venue_f_h_values.append(venue_h_values[-1])
                        venue_f_h_dates.append(venue_h_dates[-1])
                    venue_f_h_values.append(current_h)
                    venue_f_h_dates.append(gig.date)
                else:
                    venue_h_values.append(current_h)
                    venue_h_dates.append(gig.date)

        self.n_graphs += 1

        fig, ax = plt.subplots()

        artist_line1 = plt.plot(artist_h_dates,artist_h_values,color=self.colour1) #,linewidth=2.0)
        artist_line2 = plt.plot(artist_f_h_dates,artist_f_h_values,color=self.colour1,ls='--') #,linewidth=2.0)
        artist_dots1 = plt.plot(artist_h_dates,artist_h_values,color=self.colour2,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)

        venue_line1 = plt.plot(venue_h_dates,venue_h_values,color=self.colour4) #,linewidth=2.0)
        venue_line2 = plt.plot(venue_f_h_dates,venue_f_h_values,color=self.colour4,ls='--') #,linewidth=2.0)
        venue_dots1 = plt.plot(venue_h_dates,venue_h_values,color=self.colour2,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)

        years = [ date(y[0],1,1) for y in self.gig_data.get_unique_years() ]
        plt.xticks(years,[xx.strftime("%y") for xx in years])

        plt.legend((venue_line1[0],artist_line1[0]), ('Venue h-index', 'Artist h-index'), loc='upper left')

        ax.set_axisbelow(True)

        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim([datetime.strptime(str(years[0].year-1),"%Y"),
                  datetime.strptime(str(years[-1].year+1),"%Y")])

        plt.ylim( bottom=0, top=max(artist_h_values + venue_h_values) + 1 )

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
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
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
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

        for (y,c) in gigs_by_year:
            # running_total += 1 # comment this out for cumulative annual count
            years.append(datetime.strptime(str(y),"%Y"))
            for g in c:
                if end_date and g.date > end_date:
                    continue
                running_total += 1
                totals.append(running_total)
                dates.append(g.date.date())

        if len(totals) > 0:
            today = datetime.today()
            totals.append(totals[-1])
            dates.append(today.date())
            
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

        plt.ylim([0, 700])
        #from matplotlib.ticker import MultipleLocator
        #ax.yaxis.set_major_locator(MultipleLocator(50))

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()

        if False:
            import numpy as np
            from scipy.interpolate import splrep, splev

            def moving_average(a, n=3):
                ret = np.cumsum(a, dtype=float)
                ret[n:] = ret[n:] - ret[:-n]
                return ret[n - 1:] / n

            ys = moving_average(totals, 14)
            dates = dates[6:-7]

            xs = [ d.toordinal() for d in dates ]
            #ys = np.array(totals, dtype=float)
            grad = np.gradient(ys, xs)

            f = splrep(xs, ys, k=3, s=1)
            fitted = splev(xs, f)
            grad = splev(xs, f, der=1)

            # print(grad)

            fig, ax = plt.subplots()

            #line0 = plt.plot(dates[6:-7], ys)
            #line1 = plt.plot(xs, fitted)
            line2 = plt.plot(xs, grad)
            #plt.xticks(years,[xx.strftime("%y") for xx in years])

            ax.set_axisbelow(True)
            plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig("total_gradient.png")
            plt.close()
    def big_cities_by_year(self,dest=None):
        self.n_graphs += 1
        fig, ax = plt.subplots()

        years            = [ d["year"]          for d in self.stats if d["n_events"] > 0]
        total_counts     = [ d["n_events"]      for d in self.stats if d["n_events"] > 0]
        relative_counts  = [ d["n_relative"]    for d in self.stats if d["n_events"] > 0]
        dylan_counts     = [ d["n_dylan"]       for d in self.stats if d["n_events"] > 0]
        future_counts    = [ d["n_future"]      for d in self.stats if d["n_events"] > 0]
        ticket_counts    = [ d["n_future_confirmed"] for d in self.stats if d["n_events"] > 0]

        years = []
        london_counts = []
        cambridge_counts = []
        other_counts = []

        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()

        for (y,c) in gigs_by_year:
            # running_total += 1 # comment this out for cumulative annual count
            years.append(datetime.strptime(str(y),"%Y"))
            london_counts.append(0)
            cambridge_counts.append(0)
            other_counts.append(0)

            for g in c:
                if g.future: continue

                if g.city == "London":
                    london_counts[-1] += 1
                elif g.city == "Cambridge":
                    cambridge_counts[-1] += 1
                else:
                    other_counts[-1] += 1


        fig, ax = plt.subplots()

        line1 = plt.plot(years, london_counts)
        line2 = plt.plot(years, cambridge_counts)
        line3 = plt.plot(years, other_counts)

        plt.xticks(years,[xx.strftime("%y") for xx in years])

        plt.legend((line1[0],line2[0],line3[0]), 
                   ('London', 'Cambridge', 'Other'),
                   loc='upper left')

        ax.set_axisbelow(True)

        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        #plt.xlim([datetime.strptime(str(years[0].year-1),"%Y"),
                  #datetime.strptime(str(years[-1].year+1),"%Y")])

        #plt.ylim( bottom=0, top=max(artist_h_values + venue_h_values) + 1 )

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()

    def total_progress_wrt_target(self, dest=None):
        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()
        target = 40

        gig_dates = []
        gig_attainment = []

        for (y,c) in gigs_by_year:
            leap = y % 4 == 0
            days_in_year = 366 if leap else 365
            gig_count = 0
            for g in c:
                gig_count += 1
                d = g.date.date()
                ordinal = d.timetuple().tm_yday
                expected = (target / days_in_year) * ordinal
                gig_dates.append(d)
                gig_attainment.append(gig_count - expected)
                print(d, expected, gig_count - expected)

        fig, ax = plt.subplots()
        line1 = plt.plot(gig_dates, gig_attainment, color=self.colour1) #,linewidth=2.0)
        ax.grid(True, which="both")
        ax.axhline(y=0)
        plt.legend((line1[0],), ('Progress towards target of %d events/year' % target,), loc='upper left')

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def average_age_evolution(self, dest=None):
        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()

        years = []

        gig_dates = []
        gig_ages = []

        total_age = 0
        gig_count = 0

        ageless = []

        for (y,c) in gigs_by_year:
            years.append(y)
            for g in c:
                d = g.date.date()
                artist = g.sets[0].artists[0]
                age = artist.age(d)

                if age:
                    gig_count += 1
                    total_age += age
                    average = total_age / gig_count
                    gig_dates.append(d)
                    gig_ages.append(average)
                elif artist in ageless:
                    pass
                else:
                    print("No age for: " + artist.name)
                    ageless.append(artist)

        years = [ date(y,1,1) for y in years ]
                
        fig, ax = plt.subplots()
        line1 = plt.plot(gig_dates, gig_ages, color=self.colour1) #,linewidth=2.0)

        plt.xticks(years, [str(d.year)[2:4] for d in years] )
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.legend((line1[0],), ('Average age of headliners',), loc='upper right')

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
        pass
    def age_range_by_year(self, dest=None):
        gigs_by_year = self.gig_data.get_unique_years()
        gigs_by_year.sort()

        new_hdl_ages_in_year = {}
        hdl_ages_in_year = {}
        all_ages_in_year = {}

        headliners_seen = set()

        for (y,c) in gigs_by_year:
            hdl_ages_in_year[y] = []
            all_ages_in_year[y] = []
            new_hdl_ages_in_year[y] = []

            for g in c:
                d = g.date.date()
                artist = g.sets[0].artists[0]
                age = artist.age(d)

                if age:
                    hdl_ages_in_year[y].append(age)

                    if artist not in headliners_seen:
                        headliners_seen.add(artist)
                        new_hdl_ages_in_year[y].append(age)

                for s in g.sets:
                    for artist in s.artists:
                        age = artist.age(d)

                        if age:
                            all_ages_in_year[y].append(age)

        years = list(hdl_ages_in_year.keys())
        years.sort()
        hdl_ages_min = []
        hdl_ages_max = []
        hdl_ages_ave = []

        new_hdl_ages_min = []
        new_hdl_ages_max = []

        all_ages_min = []
        all_ages_max = []

        for y in years:
            new_hdl_ages = new_hdl_ages_in_year[y]
            hdl_ages = hdl_ages_in_year[y]
            total = sum(hdl_ages)
            average = total / len(hdl_ages_in_year[y])

            if new_hdl_ages:
                new_hdl_ages_min.append(min(new_hdl_ages))
                new_hdl_ages_max.append(max(new_hdl_ages) - min(new_hdl_ages))
            else:
                # in 2004 I didn't see any new headliners!
                new_hdl_ages_min.append(0)
                new_hdl_ages_max.append(0)

            hdl_ages_ave.append(average)
            hdl_ages_min.append(min(hdl_ages))
            hdl_ages_max.append(max(hdl_ages) - min(hdl_ages))

            all_ages = all_ages_in_year[y]
            all_ages_min.append(min(all_ages))
            all_ages_max.append(max(all_ages) - min(all_ages))

        fig, ax = plt.subplots()
        bar1 = ax.bar(years, all_ages_max, bottom=all_ages_min, align='center', 
                      color=self.colour3, edgecolor='black')
        bar2 = ax.bar(years, hdl_ages_max, bottom=hdl_ages_min, align='center', 
                      color=self.colour1, edgecolor='black')
        #bar3 = ax.bar(years, new_hdl_ages_max, bottom=new_hdl_ages_min, align='center',
                      #color=self.colour2, edgecolor='black')

        line1 = plt.plot(years, hdl_ages_ave, color=self.colour2)
        # dots1 = plt.plot(years, hdl_ages_ave, color=self.colour2, marker='o',ls='',
        #                  markeredgewidth=1,markeredgecolor=self.colour1)

        plt.xticks(years, [ str(y)[2:] for y in years ])
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        ax.set_axisbelow(True)
        plt.legend((line1[0], bar2[0], bar1[0]), 
                   ( 'Average age of headliners',
                     'Age range of headliners', 
                     'Age range of all artists', 
                   ), loc='upper left')
        plt.xlim([ years[0]-1, years[-1]+1 ])
        plt.ylim([10,100])

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
        pass
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
        ticket_dates = []
        ticket_totals = []
        ideal_dates = []
        ideal_totals = []

        if gigs == None:
            return False

        for g in gigs:
            running_total += 1
            if g.future:
                future_dates.append(g.date)
                future_totals.append(running_total)
                if g.confirmed:
                    if totals and not ticket_totals:
                        ticket_totals.append(totals[-1])
                        ticket_dates.append(dates[-1])
                    new_ticket_total = ticket_totals[-1] if ticket_totals else 0
                    ticket_dates.append(g.date)
                    ticket_totals.append(new_ticket_total + 1)
            else:
                if 'Bob Dylan' in g.get_artists():
                    bob_totals.append(running_total)
                    bob_dates.append(g.date)
                totals.append(running_total)
                dates.append(g.date)
                future_dates = [ g.date ]
                future_totals = [ running_total ]

        if len(future_dates) > 1:
            ideal_dates = [ date(year, 1, 1) ]
            ideal_totals = [ 0 ]

            while len(ideal_totals) <= 52:
                next_date = ideal_dates[-1] + timedelta(days=7)
                next_total = ideal_totals[-1] + 1
                ideal_dates.append(next_date)
                ideal_totals.append(next_total)

            #print(ideal_dates)
            #print(ideal_totals)

        months = [ date(year=year, month=x, day=1) for x in range(1,13) ]

        fig, ax = plt.subplots()

        blobs = dates[:]
        blob_totals = totals[:]

        # if len(future_dates) > 1:
        #     future_dates.append( date(year=year, month=12, day=31) )
        #     future_totals.append( future_totals[-1] )

        #dates.insert(0, date(year=year, month=1, day=1) )
        #totals.insert(0,0)
        line_past = None
        line_planned = None
        line_unconfirmed = None
        line_ideal = None

        if len(ideal_dates) > 1:
            line_ideal = plt.plot(ideal_dates, ideal_totals, ls='dotted', color='lightgreen')

        if len(dates) > 1:
            line_past = plt.plot(dates,totals,color=self.colour1) #,linewidth=2.0)

        if len(future_dates) > 1:
            line_unconfirmed = plt.plot(future_dates,future_totals,color=self.colour3,ls='--')

        if len(ticket_dates) > 1:
            line_planned = plt.plot(ticket_dates,ticket_totals,color=self.colour1,ls='--')

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

        legend_lines = []
        legend_names = []

        if line_past:
            legend_lines.append(line_past[0])
            legend_names.append('%d events' % year)

        if line_planned:
            legend_lines.append(line_planned[0])
            name = '%d tickets' % year
            legend_names.append(name)

        if line_unconfirmed:
            legend_lines.append(line_unconfirmed[0])
            name = '%d maybes' % year
            legend_names.append(name)

        if line_ideal:
            legend_lines.append(line_ideal[0])
            name = 'Target: 1 event/week'
            legend_names.append(name)


        plt.legend(legend_lines, legend_names, loc='upper left')

        max_y_axis = 45

        if year >= 2023:
            max_y_axis = 55

        plt.xlim([ date(year=year, month=1, day=1), date(year=year, month=12, day=31) ])
        plt.ylim([0,max_y_axis])
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

        # # for current year, draw straight line from 0 to 40 gigs:
        # if year == datetime.today().year:
        #     xs = [ date(year, 1, 1), date(year, 12, 31) ]
        #     ys = [ 0, 40 ]
        #     plt.plot(xs, ys, zorder=-10, color="green", linewidth=0.5)

        plt.tight_layout()
        fig.set_size_inches(*self.graph_size)
        fig.savefig(dest)
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

        event_songs = []
        for i in range(len(events)): 
            event_songs.append([])

        for song in unique_songs:
            for event in song['events']:
                index = events.index(event)
                event_songs[index].append(song['title'])

        for i in range(1,len(events)):
            new_songs[i] += new_songs[i-1]

        for i in range(0,len(events)):
            if events[i].get_artists()[0] != artist:
                support_new_songs.append(new_songs[i])
                support_dates.append(events[i].date.date())

        #print(event_idx)
        #print(new_songs)

        plot_percentage_change = True
        #plot_percentage_change = len(unique_songs) > 78
        if plot_percentage_change:
            percentage_change = []
            percentage_change_dates = []
            prev_songs = None
            for songs, event in zip(event_songs, events):
                if prev_songs:
                    n_common = len( set(songs) & set(prev_songs) )
                    try:
                        percentage = 100 * (len(songs) - n_common) / len(songs)
                    except ZeroDivisionError:
                        print(f"Zero songs for gig: {event.date} ({artist})")
                        percentage = 100
                    percentage_change.append(percentage)
                    percentage_change_dates.append(event.date)
                prev_songs = songs
        
        fig, ax = plt.subplots()
        ax.set_axisbelow(True)
        ax.margins(0.05)

        #line1 = plt.plot(event_idx,new_songs,marker='.')

        # plotting against date rather than index breaks something in plt:
        dates = [e.date.date() for e in events]
        line1 = plt.plot(dates,new_songs)
        dots1 = plt.plot(dates,new_songs,color=self.colour2,marker='o',ls='',markeredgewidth=1,markeredgecolor=self.colour1)
        dots2 = plt.plot(support_dates,support_new_songs,color=self.colour1,marker='o',ls='')

        #plt.xlim([dates[0].year, dates[-1].year])

        legend_lines = [ line1[0] ]
        legend_text = [ "Unique song count: " + artist ]

        if plot_percentage_change:
            line2 = plt.plot(percentage_change_dates, percentage_change, color=self.colour4)
            legend_lines.append(line2[0])
            legend_text.append("% change from previous")

        plt.legend(legend_lines, legend_text, loc='upper left')

        # Ensure a tick for each year:
        final_year = dates[-1].year + 1
        years = list( range( dates[0].year, final_year+1 ) )
        years = [ date( year=x, month=1, day=1 ) for x in years ]
        plt.xticks(years, [ str(x.year)[2:4] for x in years ] )

        plt.grid(b=True, which='both')

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig( dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def artist_song_histogram(self,artist,events,unique_songs,dest=None):
        frequency = {}

        for song in unique_songs:
            total = len(song['events'])
            if total in frequency:
                frequency[total] += 1
            else:
                frequency[total] = 1

        numbers = list(range(1,max(frequency.keys())+1))

        totals = []
        for number in numbers:
            if number in frequency:
                totals.append(frequency[number])
            else:
                totals.append(0)

        fig, ax = plt.subplots()
        ax.set_axisbelow(True)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
        bar1 = ax.bar( numbers, totals, align='center', color=self.colour1 )

        plt.legend( (bar1[0],), ('Song frequency distribution',))
        plt.xlim(0,numbers[-1]+1)

        plt.grid(b=True, which='both')

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig( dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def artist_songs_per_event(self,artist,events,unique_songs,dest=None):
        # plots the evolution of the songs/event ratio
        dates = []
        songs_per_event = []
        current_songs = []

        artist_events = []

        for song in unique_songs:
            artist_events += song['events']

        artist_events = list(set(artist_events))
        artist_events.sort(key=lambda e: e.date)

        for i, event in enumerate(artist_events):
            for song in unique_songs:
                if event in song['events']:
                    current_songs.append(song['title'])

            current_songs = list(set(current_songs))

            songs_per_event.append( len(current_songs) / (i+1) )
            dates.append(event.date)

        fig, ax = plt.subplots()
        ax.set_axisbelow(True)

        line1 = plt.plot(dates, songs_per_event, color=self.colour1)

        # plt.legend( (bar1[0],), ('Song frequency distribution',))
        # plt.xlim(0,numbers[-1]+1)

        plt.grid(b=True, which='both')

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig( dest)
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
        fig.canvas.manager.set_window_title("Figure %d" % self.n_graphs)

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
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
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
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
        bob_totals = []
        bob_dates = []

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

                if "Bob Dylan" in gig.get_artists():
                    bob_totals.append(totals[-1])
                    bob_dates.append(gig.date)

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
        dots2 = plt.plot(bob_dates,bob_totals,color=self.colour4,marker='o',ls='',\
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
            plt.tight_layout()
            fig.set_size_inches(*self.graph_size)
            fig.savefig(dest)
            plt.close()
        else:
            plt.show(block=False)
            plt.show()
    def artist_demographics(self,dest_ages=None,dest_av=None,dest_genders=None):
        years       = [ d["year"]                   for d in self.stats if d["n_events"] > 0]
        n_male      = [ d["n_male"]                 for d in self.stats if d["n_events"] > 0]
        n_female    = [ d["n_female"]               for d in self.stats if d["n_events"] > 0]
        n_male_h    = [ d["n_male_headliners"]      for d in self.stats if d["n_events"] > 0]
        n_female_h  = [ d["n_female_headliners"]    for d in self.stats if d["n_events"] > 0]
        y_ages      = [ d["ages"]                   for d in self.stats if d["n_events"] > 0]
        y_ages_head = [ d["ages_of_headliners"]     for d in self.stats if d["n_events"] > 0]
        y_ages_bob  = [ d["ages_of_bob"]            for d in self.stats if d["n_events"] > 0]

        ages_all = {}
        ages_head = {}
        ages_bob = {}

        for agelist in y_ages:
            for age in agelist:
                a = str(age)
                if a not in ages_all:
                    ages_all[a] = 0
                ages_all[a] += 1

        for agelist in y_ages_head:
            for age in agelist:
                a = str(age)
                if a not in ages_head:
                    ages_head[a] = 0
                ages_head[a] += 1

        for agelist in y_ages_bob:
            for age in agelist:
                a = str(age)
                if a not in ages_bob:
                    ages_bob[a] = 0
                ages_bob[a] += 1

        if ages_all and ages_head and ages_bob:
            alist = [ int(a) for a in ages_all.keys() ]
            alist.sort()
            graph_ages = list(range(min(alist),max(alist)+1))

            graph_freq_all = []
            graph_freq_head = []
            graph_freq_bob = []

            for age in graph_ages:
                if str(age) in ages_all:
                    graph_freq_all.append(ages_all[str(age)])
                else:
                    graph_freq_all.append(0)

                if str(age) in ages_head:
                    graph_freq_head.append(ages_head[str(age)])
                else:
                    graph_freq_head.append(0)

                if str(age) in ages_bob:
                    graph_freq_bob.append(ages_bob[str(age)])
                else:
                    graph_freq_bob.append(0)

            dob = date(1983,5,6)
            graph_freq_me = []
            
            if False:
                # plot number of gigs when I was that age
                my_ages = []
                for gig in self.gig_data.gigs:
                    if gig.future: continue
                    age = gig.date.year - dob.year
                    age -= ((gig.date.month, gig.date.day) < (dob.month, dob.day))
                    my_ages.append(age)

                for age in graph_ages:
                    graph_freq_me.append(my_ages.count(age))

                #print(graph_ages[0])
                #print(graph_freq_me)

            fig, ax = plt.subplots()
            ax.set_axisbelow(True)
            #ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            bar0 = ax.bar(graph_ages, graph_freq_all, width=1, align='center', \
                          color=self.colour1, edgecolor="black")
            bar1 = ax.bar(graph_ages, graph_freq_head, width=1, align='center', \
                          color=self.colour2, edgecolor="black")
            bar2 = ax.bar(graph_ages, graph_freq_bob, width=1, align='center', \
                          color=self.colour4, edgecolor="black")

            if graph_freq_me:
                dots = ax.scatter(graph_ages, graph_freq_me, marker="*", color=self.colour4)

            plt.grid(b=True, which='both') #, color='0.65',linestyle='-')

            plt.legend( (bar0[0],bar1[0],bar2[0]), \
                        ('Ages', 'of headliners', 'of Dylan'), \
                        loc='upper right', ncol=1, fontsize="small")

            if dest_ages:
                plt.tight_layout()
                fig.set_size_inches(*self.graph_size)
                fig.savefig(dest_ages)
                plt.close()
            else:
                plt.show(block=False)
                plt.show()

        if n_male_h and n_female_h:
            #width = 0.35
            fig, ax = plt.subplots()
            ax.set_axisbelow(True)

            butterfly_plot_with_support = False

            if butterfly_plot_with_support:
                n_female = [ -x for x in n_female ]
                n_female_h = [ -x for x in n_female_h ]

                bar1 = plt.bar(years, n_male, align='center', color=self.colour3, edgecolor='black')
                bar2 = plt.bar(years, n_male_h, align='center', color=self.colour1, edgecolor='black')
                bar3 = plt.bar(years, n_female, align='center', color=self.colour3, edgecolor='black')
                bar4 = plt.bar(years, n_female_h, align='center', color=self.colour1, edgecolor='black')
                #plt.ylim(bottom=-65, top=65)
            else:
                offset = 0.2
                years_dec = [ y - offset for y in years ]
                years_inc = [ y + offset for y in years ]
                bar_m = plt.bar(years_dec, n_male_h,   width=0.4, align='center', color=self.colour1, edgecolor='black')
                bar_f = plt.bar(years_inc, n_female_h, width=0.4, align='center', color=self.colour2, edgecolor='black')
                plt.ylim(bottom=0)

            plt.xticks(years,[str(xx)[2:] for xx in years])
            plt.grid(b=True, axis='y', which='both') #, color='0.65',linestyle='-')

            plt.xlim([years[0]-1, years[-1]+1])
            plt.legend( (bar_m[0],bar_f[0]), \
                        ('Male headliners', 'Female headliners'), \
                        loc='upper left' )

            if dest_genders:
                plt.tight_layout()
                fig.set_size_inches(*self.graph_size)
                fig.savefig(dest_genders)
                plt.close()
            else:
                plt.show(block=False)
                plt.show()

    def distance_from_previous(self,dest):
        # plot distance from previous
        vdata = self.gig_data.get_venue_data()
        #print(vdata)

        dates = []
        distances = []
        prev_coords = None
        units = "miles"

        extreme_nsew = [None, None, None, None]
        extreme_gigs = [None, None, None, None]

        missing_venue_coords = []

        annotations = []

        n_gigs = 0

        for gig in self.gig_data.gigs:
            if gig.future: continue
            n_gigs += 1

            try:
                coordinates = vdata[gig.venue]["coordinates"]
            except KeyError:
                missing_venue_coords.append(gig.venue)
                continue

            #print(coordinates)

            if prev_coords:
                distance = self.haversine(coordinates, prev_coords, units)
                #print("Distance from previous: %.2f %s" % (distance, units))
                distances.append(distance)
                dates.append(gig.date)

                if distance > 200:
                    if gig.country != "UK" or gig.city in ( "Edinburgh", "Belfast" ):
                        print(f"Annotate: {gig.city} {gig.date.year}")
                        annotation = { "city": gig.city,
                                       "date": gig.date,
                                       "distance": distance
                                      }
                        annotations.append(annotation)

            if not extreme_nsew[0] or coordinates[0] > extreme_nsew[0]:
                extreme_nsew[0] = coordinates[0]
                extreme_gigs[0] = gig

            if not extreme_nsew[1] or coordinates[0] < extreme_nsew[1]:
                extreme_nsew[1] = coordinates[0]
                extreme_gigs[1] = gig

            if not extreme_nsew[2] or coordinates[1] > extreme_nsew[2]:
                extreme_nsew[2] = coordinates[1]
                extreme_gigs[2] = gig

            if not extreme_nsew[3] or coordinates[1] < extreme_nsew[3]:
                extreme_nsew[3] = coordinates[1]
                extreme_gigs[3] = gig

            prev_coords = coordinates

        if missing_venue_coords:
            msg = f"Missing coordinates for {len(missing_venue_coords)} venues:"
            msg += ",".join(missing_venue_coords)
            raise msg

        print("Furthest North (Latitude %.2f):  %s" % (extreme_nsew[0], extreme_gigs[0].venue))
        print("Furthest South (Latitude %.2f):  %s" % (extreme_nsew[1], extreme_gigs[1].venue))
        print("Furthest East  (Longitude %.2f): %s" % (extreme_nsew[2], extreme_gigs[2].venue))
        print("Furthest West  (Longitude %.2f): %s" % (extreme_nsew[3], extreme_gigs[3].venue))
        print()

        total_distance = sum(distances)

        if units == "km":
            equators = total_distance / 40075
        elif units in ("mi", "miles"):
            equators = total_distance / 24901
        else:
            raise Exception("Invalid unit: " + units)

        print("Total distance travelled: %.2f %s = %.2f equators" % (total_distance, units, equators))
        average = total_distance / n_gigs

        text = f"Total distance travelled for {n_gigs} events:" \
               + f"\n= {total_distance:.2f} {units}" \
               + f"\n= {equators:.2f} earth circumferences" \
               + f"\n= {average:.2f} {units} per event"

        y_label = f"Geodesic distance from previous ({units})"

        self.plot_by_year(dates, distances, y_label, dest, text, annotations)
    def haversine(self, latlong1, latlong2, units="km"):
        # return great circle distance in kilometers between two points 
        import math

        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians,# [lon1, lat1, lon2, lat2])
                                     [ latlong1[1], latlong1[0], latlong2[1], latlong2[0] ] )

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 

        if units == "km":
            radius = 6371
        elif units in ("mi", "miles"):
            radius = 3956
        else:
            raise Exception("Invalid unit: " + units)

        return c * radius
    def plot_by_year(self, dates, values, ylabel, dest, text_box=None, annotations={}):
        fig, ax = plt.subplots()

        artist_line1 = plt.plot(dates,values) #,linewidth=2.0)

        if text_box:
            box_props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
            ax.text(0.05, 0.95, text_box, transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox=box_props)

        for a in annotations:
            a_city = a["city"]
            a_date = a["date"]
            a_distance = a["distance"]
            #label = f"{a_city} {a_date.year}"
            label = a_city
            coords = ( a_date, a_distance )
            label_coords = ( 0, 25 ) # offset pixels
            align = "center"

            if a_city == "New York":
                label_coords = ( -40, -10 ) # offset pixels

            if a_city == "Bergamo":
                label_coords = ( 0, 50 )

            if a_city == "Kilkenny" or a_city == "Paris":
                label_coords = ( 20, 30 )

            if a_city == "Edinburgh" and a_date.year == 2008:
                align = "left"

            if a_city == "Edinburgh" and a_date.year == 2023:
                align = "right"


            ax.annotate( label, xy=coords, xycoords='data',
                    xytext=label_coords, textcoords='offset pixels',
                    #arrowprops=dict(facecolor='black', shrink=0.05),
                    horizontalalignment=align, verticalalignment='top')

        plt.ylabel(ylabel)

        import matplotlib.dates as mdate

        years = [ d.year for d in dates ]
        years = list(set(years))
        years.append( years[-1] + 1 )
        years.sort()
        xlabels = [ str(y)[2:] for y in years ]
        years = [ date(y, 1, 1) for y in years ]
        plt.xticks( years, xlabels )

        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        plt.xlim([ years[0], years[-1] ])
        plt.ylim( bottom=-50, top=3500 )

        ax.fill_between(dates, 0, values)

        #graph_size = (13, 6) # not the usual graph size
        graph_size = self.graph_size
        graph_size = ( 3*graph_size[0], 1.5*graph_size[1] ) # double the x-range

        if dest:
            plt.tight_layout()
            fig.set_size_inches(*graph_size)
            fig.savefig(dest, bbox_inches='tight')
            plt.close()
        else:
            plt.show(block=False)
            plt.show()

