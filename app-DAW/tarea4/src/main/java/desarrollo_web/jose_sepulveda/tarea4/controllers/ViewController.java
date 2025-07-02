package desarrollo_web.jose_sepulveda.tarea4.controllers;

import desarrollo_web.jose_sepulveda.tarea4.services.ActivityDto;
import desarrollo_web.jose_sepulveda.tarea4.services.ActivityService;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class ViewController {

    private final ActivityService activityService;

    public ViewController(ActivityService service) {
        this.activityService = service;
    }

    @GetMapping("/")
    public String home() {
        return "index";
    }

    @GetMapping("/actividades/terminadas")
    public String actividadesTerminadas(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            Model model) {
        Page<ActivityDto> actividadesPage = activityService.finishedPaginated(page, size);
        model.addAttribute("actividadesPage", actividadesPage);
        model.addAttribute("pageTitle", "Listado de actividades");
        return "listado_actividades";
    }
}
