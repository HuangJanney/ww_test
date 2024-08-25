import os
import shutil


class FileUtil(object):
    CONFIG_DIR = 'config'
    LOG_DIR = 'logs'
    ASSETS_DIR = 'assets'
    IMG_DIR = 'img'
    TABLE_DIR = 'table'
    RESULT_DIR = 'results'
    SNAPSHOT_DIR = 'snapshots'
    REPORT_DIR = 'report'
    FONT_DIR = 'font'
    VIDEO_DIR = 'videos'

    CONFIG_FILE_SUFFIX = ['ini', 'cfg', 'json','yaml']
    IMG_FILE_SUFFIX = ['png']
    TABLE_FILE_SUFFIX = ['xlsx', 'xls']
    HTML_FILE_SUFFIX = ['html']
    FONT_FILE_SUFFIX = ['ttf']


    @classmethod
    def get_project_root_path(cls):
        project_name = 'ww_test'#该处需与项目文件夹名称一致
        cur_path = os.getcwd()
        root_path = cur_path[:cur_path.find(project_name) + len(project_name)]
        return root_path

    @classmethod
    def get_full_path(cls, filename):
        file_type = os.path.splitext(filename)[-1][1:]
        project_root = cls.get_project_root_path()
        if file_type in cls.CONFIG_FILE_SUFFIX:
            return os.path.join(project_root, cls.CONFIG_DIR, filename)
        elif file_type in cls.TABLE_FILE_SUFFIX:
            return os.path.join(project_root, cls.CONFIG_DIR, cls.TABLE_DIR, filename)
        return filename

    @classmethod
    def get_report_path(cls,*subdir):
        report_dir = os.path.join(cls.get_project_root_path(), cls.REPORT_DIR)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        return report_dir

    @classmethod
    def get_img_path(cls, *subdir):
        return os.path.join(cls.get_project_root_path(), cls.ASSETS_DIR, cls.IMG_DIR, *subdir)
    
    @classmethod
    def get_font_path(cls, *subdir):
        return os.path.join(cls.get_project_root_path(), cls.ASSETS_DIR, cls.FONT_DIR, *subdir)
    

    @classmethod
    def get_log_path(cls, filename):
        log_save_dir = os.path.join(cls.get_project_root_path(), cls.LOG_DIR)
        if not os.path.exists(log_save_dir):
            os.mkdir(log_save_dir)
        return os.path.join(log_save_dir, filename)

    @classmethod
    def get_result_dir(cls):
        result_dir = os.path.join(cls.get_project_root_path(), cls.RESULT_DIR)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        return result_dir

    @classmethod
    def get_snapshot_path(cls, filename, *subdir):
        snapshot_save_dir = os.path.join(cls.get_result_dir(), cls.SNAPSHOT_DIR, *subdir)
        if not os.path.exists(snapshot_save_dir):
            os.makedirs(snapshot_save_dir)
        return os.path.join(snapshot_save_dir, filename)

    @classmethod
    def list_img_filenames(cls, suffix, *subdir):
        result_filenames = []
        for root, dirs, filenames in os.walk(cls.get_img_path(*subdir), topdown=True):
            for filename in filenames:
                if os.path.splitext(filename)[-1][1:] == suffix:
                    result_filenames.append(os.path.join(os.getcwd(), root, filename))
        return result_filenames

    @classmethod
    def recreate_dir(cls, dir_path):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)

    @classmethod
    def get_file_name(cls, file_path):
        return os.path.basename(file_path)
    

    @classmethod
    def get_video_dir(cls, *subdir):
        video_dir = os.path.join(cls.get_result_dir(), cls.VIDEO_DIR, *subdir)
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        return video_dir

    @classmethod
    def get_video_path(cls, filename, *subdir):
        return os.path.join(cls.get_video_dir(*subdir), filename)    


if __name__ == '__main__':
    filenames = FileUtil.list_img_filenames('png', 'Temp')
    for filename in filenames:
        name = FileUtil.get_file_name(filename)
        print(name.split('_')[0])
