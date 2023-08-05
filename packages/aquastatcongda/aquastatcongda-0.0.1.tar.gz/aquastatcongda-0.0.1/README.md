This is the aquastat package, which includes six major functions: 

1. time_slice(df, time_period)

2. country_slice(df, country)

3. variable_slice(df, variable)

4. time_series(df, country, variable)

5. plot_heatmap(df,
                 title='',
                 xlabel=None,
                 ylabel=None,
                 label_size=20,
                 tick_label_size=16,
                 cmap=None,
                 xticklabels=None,
                 yticklabels=None,
                 figsize=None,
                 xrotation=90,
                 yrotation=0,
                 **kwargs)
 
 6. plot_histogram(df,
                   column,
                 title='',
                 xlabel=None,
                 ylabel=None,
                 label_size=20,
                 tick_label_size=16,
                 color='#0085ca',
                 alpha=0.8,
                 figsize=None,
                 **kwargs)