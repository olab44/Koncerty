import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-overlay-add-composition',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './overlay-add-composition.component.html',
  styleUrl: './overlay-add-composition.component.css'
})
export class OverlayAddCompositionComponent {
  @Output() close = new EventEmitter<void>()

  closeOverlay() {
    this.close.emit()
  }
}
