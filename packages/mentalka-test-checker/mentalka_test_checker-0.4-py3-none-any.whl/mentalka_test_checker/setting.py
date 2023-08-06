import os
import logging


scale_percent = 40  # percent of original size
predict_img_size = 28
# mark
mark_size = 16
correct_mark_color = (0, 200, 0)#(176, 255, 80)
wrong_mark_color = (0, 0, 200)
mark_thickness = 2
DONT_SHOW = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

log_path = os.path.join(BASE_DIR, 'logs/app.log')
logging.basicConfig(filename=log_path, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
