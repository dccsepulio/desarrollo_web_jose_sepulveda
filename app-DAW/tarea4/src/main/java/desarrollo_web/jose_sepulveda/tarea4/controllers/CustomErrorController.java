package desarrollo_web.jose_sepulveda.tarea4.controllers;

import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.boot.web.servlet.error.ErrorController;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.RequestDispatcher;
import org.springframework.ui.Model;

import org.springframework.stereotype.Controller;

@Controller
public class CustomErrorController implements ErrorController {

    @RequestMapping("/error")
    public String handleError(HttpServletRequest request, Model model) {
        Object status = request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);
        if (status != null && Integer.parseInt(status.toString()) == 404) {
            return "404";
        }
        Object ex = request.getAttribute(RequestDispatcher.ERROR_EXCEPTION);
        model.addAttribute("error", ex != null ? ex.toString() : null);
        return "500";
    }
}

