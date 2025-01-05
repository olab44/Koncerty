import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
import { EventCreate, GroupInfo } from '../../interfaces';
import { SessionStateService } from '../../services/session-state/session-state.service';

@Component({
  selector: 'app-overlay-new-event',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule],
  templateUrl: './overlay-new-event.component.html',
  styleUrl: './overlay-new-event.component.css'
})
export class OverlayNewEventComponent {
  @Output() close = new EventEmitter<void>()
  @Output() refresh = new EventEmitter<void>()
  group!: GroupInfo

  event: EventCreate = {
    name: '',
    type: 'Koncert',
    description: '',
    date_start: '',
    date_end: '',
    location: '',
    parent_group: -1,
    groups_participating: [],
    users_participating: [],
    setlist: []
  }

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
      this.event.parent_group = group.group_id
    });
  }

  compositions = []
  added_email = ""
  allChecked = false
  eventMessage: string = '...'
  validDates: boolean = false

  validateDates(): void {
    if (!this.event.date_start || !this.event.date_end) { this.validDates = false }
    else {
      const start = new Date(this.event.date_start);
      const end = new Date(this.event.date_end);
      if (end <= start) {
        this.eventMessage = "End date should come after the start date."
        this.validDates = false
      }
      else {
        this.eventMessage = "..."
        this.validDates = true
      }
    }
  }

  onGroupCheckboxChange(event: Event, groupId: number): void {
    const checkbox = event.target as HTMLInputElement;
    if (checkbox.checked) {
      if (groupId == this.group.group_id) {this.allChecked = true}
      this.event.groups_participating.push(groupId);
    } else {
      if (groupId == this.group.group_id) {this.allChecked = false}
      this.event.groups_participating = this.event.groups_participating.filter(
        id => id !== groupId
      );
    }
  }

  allSelected(): boolean {
    return this.event.groups_participating.includes(this.event.parent_group)
  }

  addParticipant(email: string) {
    if (!this.event.users_participating.includes(email)) {
      this.event.users_participating.push(email);
    }
  }
  removeParticipant(email: string) {
    this.event.users_participating = this.event.users_participating.filter(mail => mail !== email)
  }

  createEvent() {
    console.log(this.event)
    this.backend.postRequest('events/createEvent', this.event)
    .subscribe({
        next: res => {
          this.eventMessage = "New event organised!"
          this.refresh.emit()
        },
        error: e => {
          this.eventMessage = e.message
          console.log(e)
        }
    })
  }

  closeOverlay() {
    this.close.emit()
  }
}
