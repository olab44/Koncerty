import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
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

  message = {
    subject: '',
    content: '',
    recipient: ''
  };

  messageStatus: string = '...';

  constructor(private backend: BackendService, private state: SessionStateService) {}

  sendMessage() {
    this.backend.postRequest('announcements/createAnnouncement', this.message)
      .subscribe({
        next: (res) => {
          this.messageStatus = "Message sent successfully!";
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
