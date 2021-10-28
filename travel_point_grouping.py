import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


dest_coord = [[0, (24.993484, 121.497134)], 
                [1, (25.0007671, 121.4879088)], 
                [3, (24.9986295, 121.5007544)], 
                [2, (24.99663, 121.4869139)]]

def get_cartesian(lat=None,lon=None):
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371 # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R *np.sin(lat)
    return x,y,z
    

def wgs84_to_cartesian(wgs84_points):
    cart_coord = dict()
    for i in range(len(wgs84_points)):
        id, (lat, long) = wgs84_points[i]
        x, y, z = get_cartesian(lat=lat,lon=long)
        cart_coord[id] = (x,y,z)
    return cart_coord

def grouping(cart_coord, wgs84_points=None):
    x = list()
    y= list()
    for i in cart_coord.keys():
        x.append(cart_coord[i][0])
        y.append(cart_coord[i][1])
    df = pd.DataFrame(
        {
            'x':x,
            'y':y
        }
    )
    
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(df)
    labels = kmeans.predict(df)
    centroids = kmeans.cluster_centers_
    
    
    colmap = {1:'r',2:'g',3:'b'}
    fig = plt.figure(figsize=(5,5))
    colors = map(lambda x: colmap[x+1], labels)
        
    plt.scatter(df['x'], df['y'], color=list(colors), alpha=0.5, edgecolor='k')
    for idx, centroid in enumerate(centroids):
        plt.scatter(*centroid, color=colmap[idx+1])
    plt.xlim(df['x'].min()-1, df['x'].max()+1)
    plt.ylim(df['y'].min()-1, df['y'].max()+1)
    plt.show()
    
    # print(wgs84_points)
    
    df['id'] = cart_coord.keys()
    df['group'] = labels
    
    if wgs84_points != None:
        df.set_index('id', inplace=True)
        for i in range(len(wgs84_points)):
            id, (lat, long) = wgs84_points[i]
            df.loc[id,'lat'] = lat
            df.loc[id, 'long'] = long
    return df
        
    
    

def main():
    cart_coord = wgs84_to_cartesian(dest_coord)
    grouping(cart_coord, dest_coord)
    print(cart_coord)
    
if __name__ == '__main__':
    main()  
    
