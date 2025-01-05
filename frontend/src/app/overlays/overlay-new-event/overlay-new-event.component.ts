import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
import { EventCreate } from '../../interfaces';

@Component({
  selector: 'app-overlay-new-event',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule],
  templateUrl: './overlay-new-event.component.html',
  styleUrl: './overlay-new-event.component.css'
})
export class OverlayNewEventComponent {
  @Output() close = new EventEmitter<void>()
  @Input() group_id!: number

  event: EventCreate = {
    name: '',
    description: '',
    date_start: '',
    date_end: '',
    location: '',
    groups_participating: [],
  }

  participant_groups = [{group_id: 2, group_name: "HELLO"}, {group_id: 4, group_name: "HELLOv2"}]

  constructor(private backend: BackendService) {
  }

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
      this.event.groups_participating.push(groupId);
    } else {
      this.event.groups_participating = this.event.groups_participating.filter(
        id => id !== groupId
      );
    }
  }

  createEvent() {
    console.log(this.event)
    this.backend.postRequest('events/createEvent', this.event)
    .subscribe({
        next: res => {
          this.eventMessage = "New event organised!"
        },
        error: e => {
          this.eventMessage = e.error.detail
          console.log(e)
        }
    })
  }

  closeOverlay() {
    this.close.emit()
  }
}
