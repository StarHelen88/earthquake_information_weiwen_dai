from earthquake_information_weiwen_dai import earthquake_information_weiwen_dai

import pandas as pd
import pytest
@pytest.mark.parametrize('f_start, f_end, f_location, expected', [
    ('2022-12-14', '2022-12-15', ['Taiwan'], pd.DataFrame({'Date':['2022-12-15'],'Time':['04:03:16'],'Magnitude':['5.9'],'Place':['27 km SE of Hualien City, Taiwan'],'Felt_count':33.0,'Status':['reviewed'],'CDI':7.4,'MMI': 5.799,'SIG':560,'Depth':15.613,'Longitude':23.7801,'Latitude':121.771}))])

def test_info(f_start, f_end, f_location, expected):
    get_info = earthquake_information_weiwen_dai.earthquake_info(f_start, f_end, f_location)
    info = get_info.get_earthquake_info()
    pd.testing.assert_frame_equal(info, expected), 'Function earthquake_info not pass.'
