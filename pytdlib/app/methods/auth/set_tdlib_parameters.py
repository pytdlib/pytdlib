from pytdlib.app.utils import BaseTelegram
from pytdlib.api import functions
from pytdlib.api import types


class SetTdlibParameters(BaseTelegram):

    def set_tdlib_parameters(self,
                             use_test_dc,
                             use_file_database,
                             use_chat_info_database,
                             use_message_database,
                             use_secret_chats,
                             api_id,
                             api_hash,
                             system_language_code,
                             device_model,
                             system_version,
                             application_version,
                             enable_storage_optimizer,
                             ignore_file_names,
                             files_directory: str = "",
                             database_directory: str = ""):

        return self.send(
            functions.SetTdlibParameters(
                types.TdlibParameters(
                    use_test_dc=use_test_dc,
                    database_directory=database_directory,
                    files_directory=files_directory,
                    use_file_database=use_file_database,
                    use_chat_info_database=use_chat_info_database,
                    use_message_database=use_message_database,
                    use_secret_chats=use_secret_chats,
                    api_id=api_id,
                    api_hash=api_hash,
                    system_language_code=system_language_code,
                    device_model=device_model,
                    system_version=system_version,
                    application_version=application_version,
                    enable_storage_optimizer=enable_storage_optimizer,
                    ignore_file_names=ignore_file_names
                )
            )
        )
