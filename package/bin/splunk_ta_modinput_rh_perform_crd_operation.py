##
## SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
## SPDX-License-Identifier: LicenseRef-Splunk-1-2020
##
##

import splunk.admin as admin
import os
import shutil
import base64
import subprocess

class Splunk_TA_Modinput_Test(admin.MConfigHandler):
    def setup(self):
        if self.customAction == 'delete':
            self.supportedArgs.addReqArg('file_path')
        elif self.customAction == 'read':
            self.supportedArgs.addReqArg('file_path')
            self.supportedArgs.addOptArg('base64')
        elif self.customAction == "create":
            self.supportedArgs.addReqArg('file_path')
            self.supportedArgs.addReqArg('data')
        elif self.customAction == "update":
            self.supportedArgs.addReqArg('file_path')
            self.supportedArgs.addReqArg('data')
        elif self.customAction == 'delete_dir':
            self.supportedArgs.addReqArg('dir_path')
        elif self.customAction == 'is_dir':
            self.supportedArgs.addReqArg('dir_path')
        elif self.customAction == 'execute':
            self.supportedArgs.addReqArg('command')
        return

    def handleCustom(self, confInfo):
        if self.customAction == 'delete':
            self.delete_file(confInfo)
        elif self.customAction == 'read':
            self.read_file(confInfo)
        elif self.customAction == 'create':
            self.create_file(confInfo)
        elif self.customAction == 'update':
            self.update_file(confInfo)
        elif self.customAction == 'delete_dir':
            self.delete_dir(confInfo)
        elif self.customAction == 'is_dir':
            self.is_dir(confInfo)
        elif self.customAction == 'execute':
            self.execute_command(confInfo)

    def delete_file(self, confInfo):
        file_path = self.callerArgs.data['file_path'][0]
        if os.path.exists(file_path):
            os.remove(file_path)
            confInfo['success_message'] = ('success_message', 'File {} successfully deleted'.format(file_path))

        else:
            confInfo['error_message'] = ('delete_error_message', 'File {} not found'.format(file_path))

    def read_file(self, confInfo):
        """
        reads text files. if base64 is passed as a get query the results will be returned in base64
        """
        file_path = self.callerArgs.data['file_path'][0]
        use_base64 = self.callerArgs.data.get('base64',[False])[0]

        if os.path.exists(file_path):
            with open(file_path, 'rb') as ckpt_file:
                file_content = ckpt_file.read()
                if use_base64:
                    file_content = base64.b64encode(file_content)
            confInfo['file_content'] = ('file_content', file_content.decode('utf_8'))

        else:
            confInfo['error_message'] = ('read_error_message', "File {} not found.".format(file_path))

    def create_file(self, confInfo):
        conf_file_path = self.callerArgs.data['file_path'][0]
        conf_file_data = self.callerArgs.data['data'][0]
        path_to_local = "/".join(conf_file_path.split("/")[:-1])
        if not os.path.exists(path_to_local):
            os.makedirs(path_to_local)
        with open(conf_file_path, "w") as conf_file_obj:
                conf_file_obj.write(conf_file_data)

    def update_file(self, confInfo):
        conf_file_path = self.callerArgs.data['file_path'][0]
        conf_file_data = self.callerArgs.data['data'][0]
        path_to_local = "/".join(conf_file_path.split("/")[:-1])
        if not os.path.exists(path_to_local):
            os.makedirs(path_to_local)
        with open(conf_file_path, "a") as conf_file_obj:
                conf_file_obj.write(conf_file_data)

    def is_dir(self, confInfo):
        dir_path = self.callerArgs.data['dir_path'][0]
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            confInfo['success_message'] = ('positive_response', '{} is a directory.'.format(dir_path))
        else:
            confInfo['error_message'] = ('negative_response', '{} is not a direcotry'.format(dir_path))

    def delete_dir(self, confInfo):
        dir_path = self.callerArgs.data['dir_path'][0]
        if os.path.exists(dir_path):
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                confInfo['success_message'] = ('success_message', 'Directory {} successfully deleted'.format(dir_path))
            else:
                confInfo['error_message'] = ('delete_error_message', '{} is not a direcotry'.format(dir_path))

        else:
            confInfo['error_message'] = ('delete_error_message', 'Directory {} not found'.format(dir_path))

    def execute_command(self, confInfo):
        command = self.callerArgs.data['command'][0]
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        lines = p.stdout.readlines()
        output = []
        [output.append(str(line, "utf-8")) for line in lines]
        confInfo['success_message'] = ('output', output)

if __name__ == "__main__":
    admin.init(Splunk_TA_Modinput_Test, admin.CONTEXT_APP_AND_USER)
