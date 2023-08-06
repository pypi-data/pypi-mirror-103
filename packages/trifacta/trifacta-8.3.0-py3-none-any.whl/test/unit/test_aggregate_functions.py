#  Trifacta Inc. Confidential
#
#  Copyright 2020 Trifacta Inc.
#  All Rights Reserved.
#
#  Any use of this material is subject to the Trifacta Inc., Source License located
#  in the file 'SOURCE_LICENSE.txt' which is part of this package.  All rights to
#  this material and any derivative works thereof are reserved by Trifacta Inc.


import unittest
import pandas as pd
from trifacta.transform_functions.function_definitions import stdev, to_double, to_integer, var, mode


class TestAggregateFunction(unittest.TestCase):
    def test_something(self):
        series = pd.Series([1, 2, 3, None])
        # self.assertEqual(VarPop()(series), 0.6666666666666666)
        # self.assertEqual(StdDevPop()(series), 0.6666666666666666)
        df0 = pd.read_csv(
            '/Users/trifactait/trifacta/services/ml-service/test/wrangletopython/resources/functions/aggregate-functions/variance/input.csv',
            skip_blank_lines=False, lineterminator='\n', dtype=str, encoding='UTF-8')
        df0.columns = ['column', 'column_1', 'column_2']

        df3 = pd.DataFrame({'column': df0['column'], 'new_column': df0['column_1'].apply((lambda x: to_double(x))),
                            'new_column_1': pd.Series(df0['column_2'].apply((lambda x: to_integer(x))), dtype='Int64')})
        df3.groupby(['column'], as_index=False, dropna=False).apply(
            lambda x: pd.Series({'new_column_Var_Pop': x['new_column'].mean()}))

    def test_something_1(self):
        df0 = pd.read_csv(
            '/Users/trifactait/trifacta/services/ml-service/test/wrangletopython/resources/functions/aggregate-functions/mode/input.csv',
            skip_blank_lines=False, lineterminator='\n', dtype=str, encoding='UTF-8')
        df0.columns = ['column', 'column_1', 'column_2', 'column_3']

        df3 = pd.DataFrame({'new_column': df0['column'].apply((lambda x: to_double(x))),
                            'new_column_1': df0['column_1'].apply((lambda x: to_double(x))),
                            'new_column_2': df0['column_2'].apply((lambda x: to_double(x))),
                            'new_column_3': pd.Series(df0['column_3'].apply((lambda x: to_integer(x))), dtype='Int64')})
        df4 = df3.agg({'new_column': [
            mode()], 'new_column_1': [
            mode()], 'new_column_2': [
            mode()], 'new_column_3': [
            mode()]})

if __name__ == '__main__':
    unittest.main()

