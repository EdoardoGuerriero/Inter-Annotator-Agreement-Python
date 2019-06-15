# Inter-Annotator-Agreement-Python
<p>
  Python class containing different functions to calculate the most frequently used inter annotator agreement scores (Choen K, Fleiss K, Light K, Krippendorff alpha).
</p>

<p>
  Input Format: list of pandas dataframes and name of columns containing target annotations.<br>
  <br>
  Example:<br>
  <br>
  annotator_A = {'Sentence':[1, 2, 3], 'Stance':['favor', 'against', 'favor'], 'Sentiment':['pos', 'neg', 'pos']}<br>
  df_A = pd.DataFrame.from_dict(annotator_A)<br>
  <br>
  annotator_B = {'Sentence':[1, 2, 3], 'Stance':['against', 'against', 'favor'], 'Sentiment':['neg', 'neg', 'pos']}<br>
  df_B = pd.DataFrame.from_dict(annotator_B)<br>
  <br>
  frames = [df_A, df_B]<br>
  <br>
  IAA = Inter_Annotator_Agreement(frames=frames, annotation_col='Stance', annotators_names=['A','B'])<br>
  <br>
  IAA.Choen_K()<br>
  Out: 0.39999999999999997<br>
  <br>
  IAA.Light_K()<br>
  0.39999999999999997<br>
  <br>
  IAA.Fleiss_K()<br>
  Out: 0.33333333333333326<br> 
  <br>
  IAA.Krippendorff_alpha(metric='interval')<br>
  Out: 0.4444444444444444<br>
  <br>
</p>

<p>
  References:<br>
  <br>
  Conger, A. (1980). Integration and generalization of kappas for multiple raters. Psychological Bulletin <br>
  Cohen, J. (1960). A coefficient of agreement for nominal scales. Education and Psychological Measurement <br>
  Krippendorf, K. (2003). Content Analysis: An Introduction to its Methodology. Sage Publications<br>
</p>
