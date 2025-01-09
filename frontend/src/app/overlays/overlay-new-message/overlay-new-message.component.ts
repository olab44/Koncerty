import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
import { ForumMessageCreate, GroupInfo } from '../../interfaces';
import { SessionStateService } from '../../services/session-state/session-state.service';

@Component({
  selector: 'app-overlay-new-message',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule],
  templateUrl: './overlay-new-message.component.html',
  styleUrl: './overlay-new-message.component.css'
})
export class OverlayNewMessageComponent {
  @Output() close = new EventEmitter<void>()
  @Output() refresh = new EventEmitter<void>()
  group!: GroupInfo
  subgroups: any[] = []

  message: ForumMessageCreate = {
    subject: '',
    content: '',
    group_ids: [],
    subgroup_ids: [],
    user_emails: []
  }

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
    this.backend.getSubgroups(this.group.group_id).subscribe({
        next: (res) => { this.subgroups = res },
        error: (e) => { console.log(e) },
    })
  }

  added_email = ""
  allChecked = false
  messageStatus: string = '...'

  onGroupCheckboxChange(event: Event, groupId: number): void {
    const checkbox = event.target as HTMLInputElement;
    if (checkbox.checked) {
      if (groupId == this.group.group_id) {this.allChecked = true}
      this.message.group_ids.push(groupId);
    } else {
      if (groupId == this.group.group_id) {this.allChecked = false}
      this.message.group_ids = this.message.group_ids.filter(
        id => id !== groupId
      );
    }
  }

  addRecipient(email: string) {
    if (!this.message.user_emails.includes(email)) {
      this.message.user_emails.push(email);
    }
  }
  
  removeRecipient(email: string) {
    this.message.user_emails = this.message.user_emails.filter(mail => mail !== email)
  }

  sendMessage() {
    this.backend.postRequest('forum/createAnnouncement', this.message)
    .subscribe({
        next: res => {
          this.messageStatus = "Message sent!"
          this.refresh.emit()
        },
        error: e => {
          this.messageStatus = e.message
          console.log(e)
        }
    })
  }

  closeOverlay() {
    this.close.emit()
  }
}
