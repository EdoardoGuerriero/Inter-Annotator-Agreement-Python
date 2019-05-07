# Inter-Annotator-Agreement-Python
<p>
  Python class containing different functions to calculate the most frequently used inter annotator agreement scores (Choen, Fleiss, Light).
</p>

<p>
  Input Format: list of pandas dataframes and name of columns containing target annotations.<br>
  <br>
  Example:<br>
  <br>
  annotator_A = {'Sentence':[1,2,3], 'Stance':['favor','against','favor'], 'Sentiment':['pos','neg','pos']}<br>
  df_A = pd.DataFrame.from_dict(annotator_A)<br>
  <br>
  annotator_B = {'Sentence':[1,2,3], 'Stance':['against','against','favor'], 'Sentiment':['neg','neg','pos']}<br>
  df_B = pd.DataFrame.from_dict(annotator_B)<br>
  <br>
  frames = [df_A, df_B]<br>
  <br>
  IAA = Inter_Annotator_Agreement(frames, 'Stance', verbose=False)<br>
  <br>
  IAA.Choen_K()<br>
  Out: 0.39999999999999997<br>
  <br>
  IAA.Light_K()<br>
  0.39999999999999997<br>
  <br>
  IAA.Fleiss_K()<br>
  Out: 0.33333333333333326<br> 
</p>
