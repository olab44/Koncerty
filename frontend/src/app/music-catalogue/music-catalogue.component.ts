import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { OverlayAddCompositionComponent } from '../overlays/overlay-add-composition/overlay-add-composition.component';
import { CompositionInfo, GroupInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';
import { FilterPipe } from '../pipe/filter.pipe';
import { BackendService } from '../services/backend-connection/backend.service';

@Component({
  selector: 'app-music-catalogue',
  standalone: true,
  imports: [ CommonModule, FormsModule, TranslateModule, TopBarComponent, OverlayAddCompositionComponent, FilterPipe ],
  templateUrl: './music-catalogue.component.html',
  styleUrl: './music-catalogue.component.css'
})
export class MusicCatalogueComponent {
  group!: GroupInfo
  viewedComposition: CompositionInfo | null = null
  visibleOverlayComposition = false
  searchPhrase: string = ""
  compositions: CompositionInfo[] = []

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
    this.backend.getCatalogue(this.group.group_id).subscribe({
      next: (res) => {
        this.compositions = res.found},
      error: (e) => { console.log(e) }
    })
  }

  viewComposition(composition: any): void {
    this.viewedComposition = composition
  }

  toggleOverlayComposition(): void {
    this.visibleOverlayComposition = !this.visibleOverlayComposition
  }
}
