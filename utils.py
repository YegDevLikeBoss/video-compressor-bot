from enum import Enum

class ConversionType(Enum):
    SMALL_SIZE = 'small_size'
    NOTE_SIZE = 'note_size'

class ContentTypes(Enum):
    TEXT = 'text'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    ANIMATION = 'animation'
    GAME = 'game'
    PHOTO = 'photo'
    STICKER = 'sticker'
    VIDEO = 'video'
    VIDEO_NOTE = 'video_note'
    VOICE = 'voice'
    CONTACT = 'contact'
    LOCATION = 'location'
    VENUE = 'venue'
    DICE = 'dice'
    NEW_CHAT_MEMBERS = 'new_chat_members'
    LEFT_CHAT_MEMBER = 'left_chat_member'
    NEW_CHAT_TITLE = 'new_chat_title'
    NEW_CHAT_PHOTO = 'new_chat_photo'
    DELETE_CHAT_PHOTO = 'delete_chat_photo'
    GROUP_CHAT_CREATED = 'group_chat_created'
    SUPERGROUP_CHAT_CREATED = 'supergroup_chat_created'
    CHANNEL_CHAT_CREATED = 'channel_chat_created'
    MIGRATE_TO_CHAT_ID = 'migrate_to_chat_id'
    MIGRATE_TO_FROM_ID = 'migrate_from_chat_id'
    PINNED_MESSAGE = 'pinned_message'
    INVOICE = 'invoice'
    SUCCESSFUL_PAYMENT = 'successful_payment'
    CONNECTED_WEBSITES = 'connected_website'
    POLL = 'poll'
    PASSPORT_DATA = 'passport_data'
    PROXIMITY_ALERT_TRIGGERED = 'proximity_alert_triggered'
    VOICE_CHAT_SCHEDULED = 'voice_chat_scheduled'
    VOICE_CHAT_STARTED = 'voice_chat_started'
    VOICE_CHAT_ENDED = 'voice_chat_ended'
    VOICE_CHAT_PARTICIPANTS_INVITED = 'voice_chat_participants_invited'
    MESSAGE_AUTO_DELETE_TIMER_CHANGED = 'message_auto_delete_timer_changed'

    @staticmethod
    def as_list(*args):
        return [item.value for item in ContentTypes if item not in args]