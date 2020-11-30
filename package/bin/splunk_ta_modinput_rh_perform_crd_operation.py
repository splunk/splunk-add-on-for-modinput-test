import splunk.admin as admin
import os
import shutil
class Splunk_TA_Modinput_Test(admin.MConfigHandler):
    def setup(self):
        if self.customAction == 'delete':
            self.supportedArgs.addReqArg('file_path')
        elif self.customAction == 'read':
            self.supportedArgs.addReqArg('file_path')
        elif self.customAction == "create":
            self.supportedArgs.addReqArg('file_path')
            self.supportedArgs.addReqArg('data')
        elif self.customAction == "copy":
            self.supportedArgs.addReqArg('copy_from')
            self.supportedArgs.addReqArg('copy_to')
        return

    def handleCustom(self, confInfo):
        if self.customAction == 'delete':
            self.delete_file(confInfo)
        elif self.customAction == 'read':
            self.read_file(confInfo)
        elif self.customAction == 'create':
            self.create_file(confInfo)
        elif self.customAction == 'copy':
            self.copy_file(confInfo)
    
    def delete_file(self, confInfo):
        checkpoint_file_path = self.callerArgs.data['file_path'][0]
        if os.path.exists(checkpoint_file_path):
            os.remove(checkpoint_file_path)

    def read_file(self, confInfo):
        checkpoint_file_path = self.callerArgs.data['file_path'][0]
        if os.path.exists(checkpoint_file_path):
            with open(checkpoint_file_path, 'r') as ckpt_file:
                file_content = ckpt_file.read()
            confInfo['ckpt_file_content'] = ('file_content', file_content)

    def create_file(self, confInfo):
        conf_file_path = self.callerArgs.data['file_path'][0]
        conf_file_data = self.callerArgs.data['data'][0]
        path_to_local = "/".join(conf_file_path.split("/")[:-1])
        if not os.path.exists(path_to_local):
            os.makedirs(path_to_local)
        with open(conf_file_path, "w") as conf_file_obj:
                conf_file_obj.write(conf_file_data)

    def copy_file(self, confInfo):
        copy_from_file = self.callerArgs.data['copy_from'][0]
        copy_to_file = self.callerArgs.data['copy_to'][0]
        path_to_local = "/".join(conf_file_path.split("/")[:-1])
        if not os.path.exists(path_to_local):
            os.makedirs(path_to_local)
        with open(copy_from_file, "r") as readConfFile:
            conf_content = readConfFile.read()
            with open(copy_to_file, "w") as writeConfFile:
                writeConfFile.write(conf_content)


if __name__ == "__main__":
    admin.init(Splunk_TA_Modinput_Test, admin.CONTEXT_APP_AND_USER)
