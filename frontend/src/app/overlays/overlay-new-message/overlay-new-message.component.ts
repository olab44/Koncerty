import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-overlay-new-message',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './overlay-new-message.component.html',
  styleUrl: './overlay-new-message.component.css'
})
export class OverlayNewMessageComponent {
  @Output() close = new EventEmitter<void>()

  closeOverlay() {
    this.close.emit()
  }
}
