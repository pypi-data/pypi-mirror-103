def SSE_elbow(df, n_clusters=20, max_iter=500, tol=1e-04, init="random", n_init=200, algorithm='auto'):
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    inertia_values = []
    for i in range(1, n_clusters+1):
        km = KMeans(n_clusters=i, max_iter=max_iter, tol=tol, init=init, n_init=n_init, random_state=1, algorithm=algorithm)
        km.fit_predict(df)
        inertia_values.append(km.inertia_)
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(range(1, n_clusters+1), inertia_values, color='red')
    plt.xlabel('No. of Clusters', fontsize=15)
    plt.ylabel('SSE / Inertia', fontsize=15)
    plt.title('SSE / Inertia vs No. Of Clusters', fontsize=15)
    plt.grid()
    plt.show()
    
    
def silhouette_scores(df, n_clusters=20, max_iter=500, tol=1e-04, init="random", n_init=200, algorithm='auto'):
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    import matplotlib.pyplot as plt
    
    inertia_values = []
    
    for i in range(2, n_clusters+1):
        km = KMeans(n_clusters=i, max_iter=max_iter, tol=tol, init=init, n_init=n_init, random_state=1, algorithm=algorithm)
        df_kmeans =  km.fit_predict(df)
        inertia_values.append(silhouette_score(df, df_kmeans))
        
        
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(range(1, n_clusters), inertia_values, color='red')
    plt.xlabel('No. of Clusters', fontsize=15)
    plt.ylabel('Silhouette Score', fontsize=15)
    plt.title('Silhouette Score vs No. Of Clusters', fontsize=15)
    plt.grid()
    plt.show()
    
    
def plot_clusters(data,cluster_centers, n = 1, render = "browser"):
    
    import pandas as pd
    import plotly.io as pio
    import plotly.express as px
    import plotly.graph_objects as go
    
    pio.renderers.default=render
    centroides = pd.DataFrame(cluster_centers, columns=(data.columns))
    centroides = (centroides-centroides.min())/(centroides.max()-centroides.min())
    centroides.loc[cluster_centers.shape[0]] = list(centroides.mean())
    
    for i in range(n):
        
        fig = px.line_polar(
                    r=centroides.loc[i].values,
                    theta=centroides.columns,
                    line_close=True,
                    range_r = [0,1],
                    title="Cluster - %s" %i)
    
        fig.add_trace(go.Scatterpolar(
                                r=centroides.loc[10].values,
                                theta=centroides.columns,
                                fill='toself',
                                name="Media",
                                showlegend=True,
                                ))


        fig.show()


