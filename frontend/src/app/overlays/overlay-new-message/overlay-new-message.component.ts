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
  styleUrls: ['./overlay-new-message.component.css']
})
export class OverlayNewMessageComponent {
  @Output() close = new EventEmitter<void>();
  @Output() refresh = new EventEmitter<void>();
  group!: GroupInfo;
  subgroups: any[] = [];

  message: ForumMessageCreate = {
    title: '',
    content: '',
    parent_group: -1,
    group_ids: [],
    user_ids: []
  };

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });

    this.backend.getSubgroups(this.group.group_id).subscribe({
      next: (res) => {
        this.subgroups = res;
      },
      error: (e) => {
        console.log(e);
      }
    });
  }

  added_user_id: number | null = null;
  allChecked = false;
  messageStatus: string = '...';

  onGroupCheckboxChange(event: Event, groupId: number): void {
    const checkbox = event.target as HTMLInputElement;
    if (checkbox.checked) {
      if (groupId === this.group.group_id) { this.allChecked = true; }
      this.message.group_ids.push(groupId);
    } else {
      if (groupId === this.group.group_id) { this.allChecked = false; }
      this.message.group_ids = this.message.group_ids.filter(id => id !== groupId);
    }
  }

  addRecipient(user_id: number | null) {
    if (user_id !== null && !this.message.user_ids.includes(user_id)) {
      this.message.user_ids.push(user_id);
    }
  }

  removeRecipient(user_id: number) {
    this.message.user_ids = this.message.user_ids.filter(id => id !== user_id);
  }

  sendMessage() {
    const alertPayload = {
      title: this.message.title,
      content: this.message.content,
      parent_group: this.group.group_id,
      group_id: this.message.group_ids.length > 0 ? this.message.group_ids[0] : null,
      user_id: null,
      user_ids: this.message.user_ids.length > 0 ? this.message.user_ids : null
    };

    this.backend.postRequest('forum/createAlert', alertPayload).subscribe({
      next: (res: any) => {
        const createdAlert = {
          id: res.id,
          title: res.title,
          content: res.content,
          group_ids: res.group_ids,
          subgroup_ids: res.subgroup_ids,
        };

        this.messageStatus = `Alert created! ID: ${createdAlert.id}`;
        this.refresh.emit();
      },
      error: (e) => {
        this.messageStatus = e.message;
        console.log(e);
      }
    });
  }

  closeOverlay() {
    this.close.emit();
  }
}
