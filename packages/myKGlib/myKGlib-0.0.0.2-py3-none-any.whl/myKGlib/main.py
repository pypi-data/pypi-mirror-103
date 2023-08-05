import pandas as pd

from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
import networkx as nx
import folium
from anytree import Node, RenderTree
from wordcloud import WordCloud, STOPWORDS


from imageio import imread
import re
import time

from .bubbleChart import BubbleChart

class vizKG:
  """
  Instantiate vizKG object.
  
  Attributes:
      sparql_query (string): The SPARQL query to retrieve.
      sparql_service_url (string): The SPARQL endpoint URL.
      mode (string): Type of visualization
                     Default = 'table'
                     Options = {"table", "imageGrid", "Timeline"}.
      dataframe (pandas.Dataframe): The data table                 
  """

  def __init__(self, sparql_query, sparql_service_url, mode='Table'):
      """
      Constructs all the necessary attributes for the vizKG object

      Parameters:
          sparql_query (string): The SPARQL query to retrieve.
          sparql_service_url (string): The SPARQL endpoint URL.
          mode (string): Type of visualization
                        Default = 'Table'
                        Options = {"Table", "ImageGrid", "Timeline"}.
          dataframe (pandas.Dataframe): The data table
      """

      self.sparql_query = sparql_query
      self.sparql_service_url = sparql_service_url
      self.mode = mode
      self.dataframe = self.query_result()
      

  def query_result(self, is_value='True'):
      """
      Query the endpoint with the given query string.

      Parameters:
          is_value (bool): The boolean to filter (dot)value column.

      Returns:
          (pandas.Dataframe) table: The Query Result      
      """

      sparql = SPARQLWrapper(self.sparql_service_url, agent="Sparql Wrapper on Jupyter example")  
      
      sparql.setQuery(self.sparql_query)
      sparql.setReturnFormat(JSON)

      # ask for the result
      result = sparql.query().convert()
      table  = json_normalize(result["results"]["bindings"])

      #extract value
      if is_value:
        df = table.filter(regex='.value')
        table = df.rename(columns = lambda col: col.replace(".value", ""))
      
      #rename column
      table = self.__rename_column(table)

      return table


  def __rename_column(self, dataframe):
      """
      Rename column of dataframe based on regex validity check

          :param (pandas.Dataframe) dataframe: The table of query result.

      Returns:
          (pandas.Dataframe) table: The result of renaming table column             
      """

      #Regex pattern
      pattern_url = r"^(?:http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$(?<!.[jpg|gif|png|JPG|PNG])" #regex url
      pattern_img = r"^http(s)?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|jpeg|gif|png|JPG|JPEG|Jpeg)$"        #regex img
      pattern_coordinate = r"^Point"
      pattern_label = r"Label$"

      for i in range (len(dataframe.columns)):
        check = dataframe[dataframe.columns[i]].iloc[0]
        if re.match(pattern_url, check):
          if 'uri' in dataframe.columns:
            if 'uri2' in dataframe.columns:
              dataframe = dataframe.rename(columns={dataframe.columns[i]: "uri_"+str(dataframe.columns[i])}, errors="raise")
            else:          
              dataframe = dataframe.rename(columns={dataframe.columns[i]: "uri2"}, errors="raise")
          else:
            dataframe = dataframe.rename(columns={dataframe.columns[i]: "uri"}, errors="raise")
        elif re.match(pattern_img, check): 
          dataframe =  dataframe.rename(columns={dataframe.columns[i]: "pic"}, errors="raise")
        elif re.match(pattern_coordinate, check):
          dataframe =  dataframe.rename(columns={dataframe.columns[i]: "coordinate"}, errors="raise")
        elif i == len(dataframe.columns)-1 and (re.match(pattern_label, check)):
          dataframe = dataframe.rename(columns={dataframe.columns[i]: dataframe.columns[i]}, errors="raise")

      #change data types in each column
      dataframe = self.__change_dtypes(dataframe)  
      
      return dataframe


  def __change_dtypes(self, dataframe):
      """
      Change data type column of dataframe

          :param dataframe (pandas.Dataframe): The result of renaming table column .

      Returns:
          (pandas.Dataframe) table: The result of changing data type table column             
      """

      for column in dataframe:
        try:
          dataframe[column] = dataframe[column].astype('datetime64')
        except ValueError:
          pass
      for column in dataframe:
        try:
          dataframe[column] = dataframe[column].astype('float64')
        except (ValueError, TypeError):
          pass
      return dataframe

  def check_property(self, dataframe):
      """
      Find candidate form for visualization

      Parameter:
          dataframe (pandas.Dataframe): The data table

      Returns:
          candidate_visualization (list): List of candidate visualization
      """

      candidate_visualization = []
      #reserved name column
      reserved_name = ['uri', 'pic', 'coordinate']

      date_column = [name for name in self.dataframe.columns if self.dataframe[name].dtypes == 'datetime64[ns]']
      integer_column = [name for name in self.dataframe.columns if self.dataframe[name].dtypes == 'float64']
      object_column = [name for name in self.dataframe.columns if not name.startswith(tuple(reserved_name)) and self.dataframe[name].dtypes == 'object']
      no_uri_column = [name for name in self.dataframe.columns if not name.startswith('uri')]
      uri_column = [name for name in self.dataframe.columns if name.startswith('uri')]

      num_date_column = len(date_column)
      num_integer_column = len(integer_column)
      num_object_column = len(object_column)
      num_no_uri_column = len(no_uri_column)
      num_uri_column = len(uri_column) 

      if 'pic' in self.dataframe.columns:
        candidate_visualization.append('ImageGrid')
      if 'coordinate' in self.dataframe.columns:
        candidate_visualization.append('Map')
      if num_date_column == 2:
        candidate_visualization.append('Timeline')
      if num_object_column == 2 and num_uri_column == 2:
        candidate_visualization.append('Graph')
        candidate_visualization.append('Tree')
      if 3 <= num_no_uri_column <= 5 :
        candidate_visualization.append('Dimensions')
      if num_object_column >= 1:
        candidate_visualization.append('WordCloud')
      if num_object_column == 1 and num_date_column == 1 and num_integer_column == 1:
        candidate_visualization.append('AreaChart')
      if num_date_column == 1 and num_integer_column == 2:
        candidate_visualization.append('StackedAreaChart')
      if num_object_column == 1 and num_integer_column == 2:
        candidate_visualization.append('ScatterChart')
      if num_date_column == 1 and num_integer_column == 1:
        candidate_visualization.append('LineChart')
      if num_object_column <= 2 and num_integer_column == 1:
        candidate_visualization.append('BarChart')
      if num_object_column == 2 and num_integer_column == 1:
        candidate_visualization.append('TreeMap')
        candidate_visualization.append('SunBurstChart')
      if num_integer_column == 1:
        candidate_visualization.append('Histogram')
        candidate_visualization.append('DensityPlot')
      if num_object_column == 1 and num_integer_column == 1:
        candidate_visualization.append('PieChart')
        candidate_visualization.append('DonutChart')
        candidate_visualization.append('BoxPlot')
        candidate_visualization.append('ViolinPlot')
        candidate_visualization.append('BubbleChart')
        candidate_visualization.append('TreeMap')
        candidate_visualization.append('SunBurstChart')
      if num_integer_column >= 3:
        candidate_visualization.append('HeatMap')
      else:
        candidate_visualization.append('Table')

      return candidate_visualization

  def plot(self):
      """
      Plot visualization with suitable corresponding mode

      """
      if len(self.dataframe) != 0:
        candidate_visualization = self.check_property(self.dataframe)

        if self.mode in candidate_visualization:
          if self.mode == 'ImageGrid':
            self.ImageGrid(self.dataframe)
          elif self.mode == 'Timeline':
            self.Timeline(self.dataframe)
          elif self.mode == 'Graph':
            self.Graph(self.dataframe)
          elif self.mode == 'Dimensions':
            self.Dimensions(self.dataframe)
          elif self.mode == 'Map':
            self.Map(self.dataframe)
          elif self.mode == 'Tree':
            self.Tree(self.dataframe)
          elif self.mode == 'WordCloud':
            self.WordCloud(self.dataframe)         
          elif self.mode == 'LineChart':
            self.LineChart(self.dataframe)
          elif self.mode == 'BarChart':
            self.BarChart(self.dataframe)
          elif self.mode == 'Histogram':
            self.Histogram(self.dataframe)
          elif self.mode == 'DensityPlot':
            self.DensityPlot(self.dataframe)
          elif self.mode == 'TreeMap':
            self.TreeMap(self.dataframe) 
          elif self.mode == 'SunBurstChart':
            self.SunBurstChart(self.dataframe)
          elif self.mode == 'HeatMap':
            self.HeatMap(self.dataframe)
          elif self.mode == 'PieChart':
            self.PieChart(self.dataframe)
          elif self.mode == 'DonutChart':
            self.DonutChart(self.dataframe)
          elif self.mode == 'BoxPlot':
            self.BoxPlot(self.dataframe)
          elif self.mode == 'ViolinPlot':
            self.ViolinPlot(self.dataframe)
          elif self.mode == 'AreaChart':
            self.AreaChart(self.dataframe)
          elif self.mode == 'StackedAreaChart':
            self.StackedAreaChart(self.dataframe)
          elif self.mode == 'ScatterChart':
            self.ScatterChart(self.dataframe)
          elif self.mode == 'BubbleChart':
            self.BubbleCharts(self.dataframe)                                           
          else:
            self.SimpleTable(self.dataframe)  
        else:
          self.SimpleTable(self.dataframe)
      else:
        print("No data was found")

  @staticmethod
  def BubbleCharts(dataframe):
    """
    Generate BubbleChart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]

    #Plot
    bubble_chart = BubbleChart(area=dataframe[integer_label],
                           bubble_spacing=0.1)

    bubble_chart.collapse()

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    bubble_chart.plot(
        ax, dataframe[object_label])
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    ax.set_title('Plot')

    plt.show()

  @staticmethod
  def ScatterChart(dataframe):
    """
    Generate ScatterChart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    integer_columns = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64']
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]
    #plot
    fig = px.scatter(dataframe, x=integer_columns[0], y=integer_columns[1], color=object_label)
    fig.show()

  @staticmethod
  def StackedAreaChart(dataframe):
    """
    Generate StackedAreaChart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    integer_columns = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64']
    date_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'datetime64[ns]'][0]
    #set index by date label
    dataframe = dataframe.set_index(date_label)
    #plot
    ax = dataframe.plot.area(stacked=True)
    plt.show(block=True)

  @staticmethod
  def AreaChart(dataframe):
    """
    Generate AreaChart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    date_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'datetime64[ns]'][0]
    #plot
    fig = px.area(dataframe, x=date_label, y=integer_label, color=object_label,line_group=object_label)
    fig.show()    

  @staticmethod
  def ViolinPlot(dataframe):
    """
    Generate ViolinPlot visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.violin(dataframe, x=object_label, y=integer_label)
    fig.show()

  @staticmethod
  def BoxPlot(dataframe):
    """
    Generate BoxPlot visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.box(dataframe, x=object_label, y=integer_label)
    fig.show()

  @staticmethod
  def DonutChart(dataframe):
    """
    Generate DonutChart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.pie(dataframe, values=dataframe.columns[-1], names=dataframe.columns[0], hole=0.3)
    fig.show()

  @staticmethod
  def PieChart(dataframe):
    """
    Generate PieChart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_label = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object'][0]
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.pie(dataframe, values=integer_label, names=object_label)
    fig.show()

  @staticmethod
  def HeatMap(dataframe):
    """
    Generate HeatMap visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #plot HeatMap
    sns.heatmap(dataframe.corr(), annot = True)
    pass

  @staticmethod
  def SunBurstChart(dataframe):
    """
    Generate sunburst chart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_columns = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object']
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.sunburst(dataframe, path=object_columns, values=integer_label)
    fig.show()

  @staticmethod
  def TreeMap(dataframe):
    """
    Generate tree map visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_columns = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object']
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.treemap(dataframe, path=object_columns, values=integer_label)
    fig.show()

  @staticmethod
  def DensityPlot(dataframe):
    """
    Generate simple density plot visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    object_column = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object']
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot multiple density plot when there is a object column
    if len(dataframe[object_column[0]].unique()) != len(dataframe):
      sns.displot(data=dataframe, x=integer_label, hue=object_column[0], kind="kde")
      pass
    else:
      sns.displot(data=dataframe, x=integer_label, kind="kde")
      pass

  @staticmethod
  def Histogram(dataframe):
    """
    Generate simple histogram visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]
    #plot
    fig = px.histogram(dataframe, x=integer_label)
    fig.show()

  @staticmethod
  def BarChart(dataframe):
    """
    Generate simple bar chart visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_column = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object']
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]

    num_object_column = len(object_column)
    num_uniq_obj_column0 = len(dataframe[object_column[0]].unique())
    num_uniq_obj_column1 = None

    #plot stacked bar when num_object_column == 2
    if num_object_column == 2:
      num_uniq_obj_column1 = len(dataframe[object_column[1]].unique())
      groupby_label = [object_column[0] if num_uniq_obj_column0 < num_uniq_obj_column1 else object_column[1]][0]
      item_label = [object_column[0] if num_uniq_obj_column0 > num_uniq_obj_column1 else object_column[1]][0]
      #plot stacked horizontal bar when unique value of item_label > 20
      if (len(item_label)) > 20:
        fig = px.bar(dataframe, x=integer_label, y=item_label, color=groupby_label, orientation='h')
        fig.show()
      else:        
        fig = px.bar(dataframe, x=item_label, y=integer_label, color=groupby_label)
        fig.show()
    else:
      item_label = object_column[0]
      #horizontal bar when unique value of item_label > 20
      if num_uniq_obj_column0 > 20:
        fig = px.bar(dataframe, x=integer_label, y=item_label,  orientation='h')
        fig.show()
      else:
        fig = px.bar(dataframe, x=item_label, y=integer_label)
        fig.show()

  @staticmethod
  def LineChart(dataframe):
    """
    Generate simple table visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #Get column name based on data type
    object_column = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object']
    date_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'datetime64[ns]'][0]
    integer_label = [name for name in dataframe.columns if dataframe[name].dtypes == 'float64'][0]

    num_object_column = len(object_column)

    if num_object_column:
      sns.lineplot(data=dataframe, x=date_label, y=integer_label, hue=object_column[0])
      pass
    else:
      fig = px.line(dataframe, x=date_label, y=integer_label)
      fig.show()

  @staticmethod
  def SimpleTable(dataframe):
    """
    Generate simple table visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    fig = ff.create_table(dataframe)
    fig.show()

  @staticmethod
  def ImageGrid(dataframe):
    """
    Generate image grid visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    pic = [i for i in dataframe.pic]

    #get label column
    labels = [name for name in dataframe.columns if name != 'uri' and name != 'pic']
    itemLabel = []
    if labels:
      itemLabel = [i for i in dataframe[labels[0]]]
    else:
      itemLabel = [i for i in dataframe.uri]

    columns = 4
    width = 20
    height = max(20, int(len(pic)/columns) * 20)
    plt.figure(figsize=(20,20))
    for i, url in enumerate(pic):
        plt.subplot(len(pic) / columns + 1, columns, i + 1)
        try:
          image = imread(url)
          plt.title(itemLabel[i])
          plt.imshow(image) #, plt.xticks([]), plt.yticks([])
          plt.axis('off')
        except:
          time.sleep(5)
          image = imread(url)
          plt.title(itemLabel[i])
          plt.imshow(image) #, plt.xticks([]), plt.yticks([])
          plt.axis('off')
  
  @staticmethod
  def Timeline(dataframe):
    """
    Generate timeline visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #get label column
    labels = [name for name in dataframe.columns if name != 'uri' and name != 'pic' and dataframe[name].dtypes != 'datetime64[ns]']
    if not labels:
      labels = [name for name in dataframe.columns if name == 'uri']
      
    #get date column
    dateLabels = [name for name in dataframe.columns if dataframe[name].dtypes == 'datetime64[ns]']

    fig = px.timeline(dataframe, x_start=dateLabels[-1], x_end=dateLabels[0], 
                      y=labels[0], color=labels[0])
    fig.update_yaxes(autorange="reversed")
    fig.show()

  @staticmethod
  def Graph(dataframe):
    """
    Generate graph visualization

    :param dataframe (pandas.Dataframe): data for visualization
    """
    #filter out column with reserved name and particular data types
    reserved_name = ['uri', 'pic', 'coordinate']
    object_column = [name for name in dataframe.columns if not name.startswith(tuple(reserved_name)) and dataframe[name].dtypes == 'object']

    #plot
    G = nx.from_pandas_edgelist(dataframe, source=object_column[0], target=object_column[1]) #, edge_attr=''
    plt.figure(figsize=(20,20))
    nx.draw_kamada_kawai(G, with_labels=True, font_weight='bold')

  @staticmethod
  def Dimensions(dataframe):
    """
    Generate dimension visualization

    :param dataframe (pandas.Dataframe): data for visualization    
    """
    dataframe_to_list = []
    for column in dataframe:
      dataframe_to_list += dataframe[column].tolist()
    
    def index_data(type_link='source'):
      """
      Return indices correspond to labels
      """
      curr_key = 0
      indices = [0]
      curr_value = dataframe_to_list[0]
      first_row = [dataframe_to_list[0]] 
      data = dataframe_to_list[:-dataframe.shape[0]]

      if type_link == 'target':
        curr_value = dataframe_to_list[dataframe.shape[0]]
        first_row = [dataframe_to_list[dataframe.shape[0]]]
        data = dataframe_to_list[dataframe.shape[0]:]

      for key,value in enumerate(data):
        if value != curr_value :
          if value in first_row:
            curr_key = first_row.index(value)
            curr_value = value
            indices.append(curr_key)
            first_row.append(curr_value)
          else:
            indices.append(key)
            first_row.append(value)
            curr_value = value
            curr_key = key
        elif value == curr_value:
          if key != 0:
            indices.append(curr_key)
            first_row.append(curr_value)
            
      if type_link == 'target':
        indices = [i+dataframe.shape[0] for i in indices]

      return indices

    #plot
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          label = dataframe_to_list,
        ),
        link = dict(
          source = index_data(type_link='source'), # indices correspond to labels, eg A1, A2, A1, B1, ...
          target = index_data(type_link='target'),
          value = [1 for i in range(len(dataframe_to_list)-dataframe.shape[0])]
      ))])

    fig.show()

  @staticmethod
  def Map(dataframe):
    """
    Generate map visualization

    :param dataframe (pandas.Dataframe): data for visualization    
    """
    dataframe['coordinate_point'] = dataframe['coordinate']
    dataframe_new = dataframe.apply(lambda S:S.str.strip('Point()'))
    new = dataframe_new[dataframe_new.columns[-1]].str.split(" ", n = 1, expand = True)
    new = new.astype('float64')
    dataframe['coordinate'] = new.apply(lambda x: list([x[1], x[0]]),axis=1)

    m = folium.Map()

    for i in range (len(dataframe)):
        folium.Marker(
            location=dataframe.coordinate[i],
            popup=dataframe.coordinate_point[i]
        ).add_to(m)

    m

  @staticmethod
  def Tree(dataframe):
    """
    Generate tree visualization

    :param dataframe (pandas.Dataframe): data for visualization    
    """
    def add_nodes(nodes, parent, child):
      if parent not in nodes:
        nodes[parent] = Node(parent)  
      if child not in nodes:
        nodes[child] = Node(child)
        nodes[child].parent = nodes[parent]
    
    nodes = {}
    for parent, child in zip(dataframe.iloc[:, -2],dataframe.iloc[:, -1]):
      add_nodes(nodes, parent, child)

    roots = list(dataframe[~dataframe.iloc[:, -2].isin(dataframe.iloc[:, -1])][dataframe.columns[-2]].unique())
    for root in roots:         # you can skip this for roots[0], if there is no forest and just 1 tree
        for pre, _, node in RenderTree(nodes[root]):
            print("%s%s" % (pre, node.name))

  @staticmethod
  def WordCloud(dataframe):
    """
    Generate tree visualization

    :param dataframe (pandas.Dataframe): data for visualization    
    """
    #Get column name with object type
    object_column = [name for name in dataframe.columns if not name.startswith(tuple(['uri', 'coordinate', 'pic'])) and dataframe[name].dtypes == 'object']

    #Merge into one column
    new_data = dataframe[object_column[0]]
    for i in range (1, len(object_column)):
        new_data += dataframe[object_column[i]]

    #Merge into one variable
    new_data = " ".join(new_data)

    #initiate wordcloud object
    stopwords = set(STOPWORDS) 
    wordcloud = WordCloud(
                    width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10
                    ).generate(new_data) 
      
    # plot the WordCloud image                        
    plt.figure(figsize = (20, 20), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0)


