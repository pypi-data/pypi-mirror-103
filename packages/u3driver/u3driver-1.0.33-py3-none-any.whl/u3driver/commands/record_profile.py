from u3driver.commands.base_command import BaseCommand

class RecordProfile(BaseCommand):
    '''
    record = 0 停止打点
    record = 1 开始打点
    '''
    def __init__(self, socket,request_separator,request_end,record):
        super(RecordProfile, self).__init__(socket,request_separator,request_end)
        self.record = record

    def execute(self):
        data = self.send_data(self.create_command('RecordProfile',self.record))
        print(data)
        