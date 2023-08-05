import pandas as pd
import numpy as np 
import getpass

# set the sf account name
sf_account = 'ra45066.eu-west-1'
from toolkit_w.snowflake.snowflakeq import Snowflakeq
SQ=Snowflakeq()

pwd = getpass.getpass("passsword:")





class Crp:
    """
    """



    def getCleanData(self,df):
        """
        Params: 
            df-> Dataframe
        -----------------------
        Output: 
            Clean dataframe after filtering
            log_file - Desc of actions taken
        """
        log_file = []
        # Clean cancelled orders 
        df['cancelledat'] = df['cancelledat'].fillna('Valid')
        df_1 = df[(df.cancelledat == 'Valid')]
        
        # Record canceled orders
        canceled_orders_num = (len(df) - len(df_1))
        
        # Clean free orders 
        free = df[(df.totaldiscounts == df.totalorderitemsprice) & (df.totalprice == 0)]
        free_orders_num = len(free)
            
        log_file.append([canceled_orders_num,free_orders_num])
        
        # log file for documentation
        log_file = pd.DataFrame(log_file,columns = ['Number_of_canceled_Orders','Number_of_free_orders'])
        
        
        df_1 = df_1[~(df_1.id.isin(free['id'].values))]
        
        return df_1,log_file

#-----------------------------------------------------------------------------------------------------------------------











    def getTrainingframe(self,df,dateFlag_sep,date_flag_min):
        """
        Params:
            df                -> Dataframe
            dateFlag_sep      -> Timestamp separator
            date_flag_min     -> Min date for training frame
        ---------------------
        Output:
        """
    #     dateFlag_sep = np.max(df['order_date']) - pd.DateOffset(months=timeFlag)
    #     date_flag_min = dateFlag_sep - pd.DateOffset(months=train_window)
        
        df = df[(df.order_date <= dateFlag_sep) & (df.order_date >= date_flag_min)]
        
        return df 

#--------------------------------------------------------------------------------------------------------------------------

    def getTargetframe(self,df,dateFlag_sep,lag):
        """
        Params:
            df           -> dataframe
            dateFlag_sep -> 
            lag          ->
        --------------------
        Output:
        
        
        """
    #     dateFlag_sep = np.max(df['order_date']) - pd.DateOffset(months=timeFlag)
        date_max = dateFlag_sep + pd.DateOffset(months=lag)
        df = df[(df.order_date > dateFlag_sep) & (df.order_date < date_max)]
        
        return df

# --------------------------------------------------------------------------------------------------------------------------

    def getTargetValues(self,train_data,target_data):
        """
        Params:
            train_data  ->
            target_data ->
        --------------------
        Output:
        
        """
        target = []
        customers_id = train_data['customerid'].unique()
        for c_id in customers_id:
            if c_id in target_data['customerid'].unique():
                value = 1
            else:
                value = 0
            target.append([c_id,value])

        target = pd.DataFrame(target,columns = ['customerid','is_returned'])
        #Output
        return target

 #---------------------------------------------------------------------------------------------------------------------------



    def getRecency(self,matrix,dateFlag):
        """
        Params:
        
            matrix -> data matrix
            dateFlag    ->
        ---------------------
        Output:- entire modified dataframe with the recency feature
        
        """
        matrix['Recency'] = matrix.apply(lambda x: dateFlag - pd.to_datetime(x.order_date),axis =1).dt.days
        
        output = matrix
        
        # Output
        return output




    def getLastOrderparams(self,matrix,train_df):
        """
        Params:
            matrix      ->
            train_df    ->
        --------------------
        Output:
            output = matrix with last order value
        """
        
        target = train_df[train_df.customerid.map(matrix['order_date']) == train_df.order_date][['customerid',
        'totalprice','totaldiscounts','totalweight']]
        matrix = matrix.reset_index().rename(columns = {'totalprice':'LastOrderValue',
                                'totaldiscounts':'LastOrderDiscount',
                                'totalweight':'LastOrderWeight'})
        output = pd.merge(target,matrix,on='customerid')
        # output.drop_duplicates(inplace = True)
        
        # Output
        return output



    def getTotalSpentLMonth(self,train_df,dateFlag_sep,df_matrix):
        """
        Params:


        -----------------
        Output:
        
        
        """

        total_spent_last_month_sep = dateFlag_sep - pd.DateOffset(months = 1)
        
        print('Last Month Money spent:',total_spent_last_month_sep)
        
        last_month_df = train_df[(train_df.order_date >= total_spent_last_month_sep - pd.DateOffset(months = 1)) & (train_df.order_date <= total_spent_last_month_sep)]
        
        last_month_spent = last_month_df.groupby('customerid').agg({'totalprice':
                                                        'sum'}).reset_index().rename(columns = {'totalprice':'LastMonthTotalSPent'})
        
        df_matrix = df_matrix.reset_index()

        df_matrix = pd.merge(df_matrix,last_month_spent,on='customerid',how = 'left')
        
        df_matrix = df_matrix.fillna(0)
        
        # df_matrix = df_matrix.rename(columns = {'totalprice':'Last_Month_Total_Spent'})
        
        
        
        output = df_matrix
        
        return output


# ----------------------------------------------------------------------------------

    def getFeaturesMatrix(self,train_df,org_df,timeFlag,items_dataset,customer_name,train_window):
        """
        Params:
            train_df -> train timeframe dataframe
            org_df   -> original dataframe with the all the needed data
            timeFlag -> date separator (between the traget period and the train period)
        ----------------
        Output: Features Matrix of the chosen timeframe
        """
        
        # Get customer ids
        customers = train_df['customerid'].unique()
        # Get the date which acts as reference point for future calculations
        dateFlag_sep = np.max(org_df['order_date']) - pd.DateOffset(months=timeFlag)
        # The date which is the min date for the feature matrix 
        date_flag_min = dateFlag_sep - pd.DateOffset(months=train_window)
        # Create a grouping aggregator
        grp = train_df.groupby('customerid')

        grp_dict = {'order_date':'max','id':'count','totalprice':'sum','buyeracceptsmarketing':'max',
                    'billingaddresscountrycode':'unique'}

        df_matrix = grp.agg(grp_dict).rename(columns={'id':'num_orders','totalprice':'TotalSpent'})
        # Recency Feature
        df_matrix = self.getRecency(df_matrix,dateFlag_sep)
        # Different Last orders parameters feature ( Discount value, weight ) 
        df_matrix = self.getLastOrderparams(df_matrix,train_df)
        # Total expenduture of the last month before date separator
        df_matrix = self.getTotalSpentLMonth(train_df,dateFlag_sep,df_matrix)


        orders_param = SQ.get_data_from_sf('V_DIFFDAYSBETWEENPURCHASESAGG',customer_name,pwd,dateFlag_sep,date_flag_min)

        output = pd.merge(df_matrix,orders_param,on='customerid')
        
        
        return output



# --------------------------------------------------------------------------------------------------------------------------------

    def getMergedDF(self,data_list,key):
        """
        Params: 
            data_list -> list that contains all dataframes
            key - string, the mutual key for the merge. 
        ---------------
        Output: Merged dataset
        
        
        """
        output = reduce(lambda  left,right: pd.merge(left,right,on=[key],
                                                how='outer'), data_list)
        
        
        return output


# ------------------------------------------------------------------------------------------------------------------------------------



    def prepareDF(self,original_dataset,dateFlag_sep,date_flag_min,lag,items_dataset,customer_name,train_window):
        """
        Params:
            original_dataset ->
            timeFlag         ->
            train_window     ->
        -------------------------------__version__
        Output:
        :")
        """
        
        # First, perform initial cleaning and save a log file of action
    
        df,log_file = self.getCleanData(original_dataset)
        # Get the first matrices
        train_data = self.getTrainingframe(df,dateFlag_sep,date_flag_min)
        print('train_data Done')
        # For the target values calculations first -> get the relevant dataframe with the relevant timeframe
        target_frame = self.getTargetframe(df,dateFlag_sep,lag)
        print('target frame done')
        # Calculate the target value
        target_value = self.getTargetValues(train_data,target_frame)
        print('target value done')
        # Calculate features
        df = self.getFeaturesMatrix(train_data,original_dataset,lag,items_dataset,customer_name,train_window)
        
        # Merge feature sets
        # data = self.getMergedDF(df,'customerid')
        #Merge with target value 
        
        finalDF = pd.merge(df,target_value,on='customerid')
        
        # finalDf = finalDF.rename(columns = {'num_orders':'Num_orders','totalprice':'Total_spent'})
        
        output =  finalDF
        
        
        return output
# -----------------------------------------------------------------------------------------------

    def buildDF(self,original_dataset,lag,train_window,items_dataset,customer_name):
        """
        Params:
            original_dataset - > the original raw data 
            lag              - > size ( in months) of the targetValue window
            train_window     - > size of the feature matrix
        Output: Constructed dataframe 
        
        """
        
        # Lower limit date
        min_date = np.min(original_dataset['order_date']) + pd.DateOffset(months = train_window)
        print('Min date for training timeframe:',min_date)
        output = []
        # Upper limit date
        date_max = np.max(original_dataset['order_date'])
        # Initial relative timeFlag
        dateFlag_sep = date_max - pd.DateOffset(months=lag)
        # Initial timeframe min date
        date_flag_min = dateFlag_sep - pd.DateOffset(months=train_window)
        print(dateFlag_sep,date_flag_min)
        # Construct dataframe according to that timeframe
        output.append(self.prepareDF(original_dataset,dateFlag_sep,date_flag_min,lag,items_dataset,customer_name,train_window))
        print(dateFlag_sep,date_flag_min)
        # Repeat the procedure until the bottom limit of the trainFrame reaches the minimum date possible according to the original dataset.
        while date_flag_min >= min_date:
        
            dateFlag_sep = dateFlag_sep - pd.DateOffset(months=lag)
            date_flag_min = dateFlag_sep - pd.DateOffset(months=train_window)
            output.append(self.prepareDF(original_dataset,dateFlag_sep,date_flag_min,lag,items_dataset,customer_name,train_window))
            print(dateFlag_sep,date_flag_min)
            
            
        return output